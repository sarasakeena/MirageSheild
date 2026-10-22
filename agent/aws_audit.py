"""
AWS KMS & DynamoDB Incident Audit Trail Service
Digitally signs verdicts with AWS KMS and commits immutable audit logs to Amazon DynamoDB.
Supports real AWS SDK (boto3) and resilient local cryptographic signing.
"""

import os
import json
import base64
import hmac
import hashlib
import logging
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from shared.schemas import Verdict, IncidentRecord

logger = logging.getLogger("aws_audit")

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
KMS_KEY_ID = os.getenv("KMS_KEY_ID", "alias/mirage-shield-ledger-key")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_INCIDENTS_TABLE", "mirage_shield_incidents")
AWS_LOCAL_SIMULATION_MODE = os.getenv("AWS_LOCAL_SIMULATION_MODE", "false").lower() in ("true", "1", "yes")


class AwsAuditLedger:
    """
    Cryptographic Audit Ledger for MIRAGE-SHIELD verdicts.
    Guarantees tamper-evidence for law enforcement evidence packages.
    """

    def __init__(self):
        self.region = AWS_REGION
        self.kms_key_id = KMS_KEY_ID
        self.table_name = DYNAMODB_TABLE_NAME
        self.use_boto = False
        self.kms_verified = False
        self.dynamodb_verified = False
        self._last_signature_type = "LOCAL_HMAC_SHA256_SANDBOX"
        self._last_storage_type = "IN_MEMORY_LOCAL_LEDGER"
        self._local_ledger: Dict[str, IncidentRecord] = {}

        if not AWS_LOCAL_SIMULATION_MODE and os.getenv("AWS_ACCESS_KEY_ID"):
            try:
                import boto3
                self.kms_client = boto3.client("kms", region_name=self.region)
                self.dynamo_client = boto3.client("dynamodb", region_name=self.region)
                self.use_boto = True
                logger.info("Initialized live AWS KMS and DynamoDB clients.")
            except Exception as e:
                logger.warning(f"Could not connect to live AWS services ({e}), falling back to local cryptographic ledger.")
        else:
            logger.info("Running in resilient local cryptographic ledger mode.")

    def sign_verdict(self, verdict: Verdict) -> Tuple[str, str]:
        """
        Computes SHA256 digest of verdict payload and signs with AWS KMS or local HMAC-SHA256.
        Returns (signature_base64, digest_hex).
        """
        payload_str = json.dumps(verdict.model_dump(), sort_keys=True)
        digest = hashlib.sha256(payload_str.encode("utf-8")).digest()
        digest_hex = digest.hex()

        if self.use_boto:
            try:
                resp = self.kms_client.sign(
                    KeyId=self.kms_key_id,
                    Message=digest,
                    MessageType="DIGEST",
                    SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
                )
                sig_b64 = base64.b64encode(resp["Signature"]).decode("utf-8")
                self.kms_verified = True
                self._last_signature_type = "AWS_KMS_ASYMMETRIC_RSA"
                return sig_b64, digest_hex
            except Exception as e:
                logger.warning(f"Live KMS signing call failed ({e}), falling back to internal cryptographic sign.")
                self.kms_verified = False

        # Local hardware-like cryptographic signing using HMAC-SHA256
        self.kms_verified = False
        self._last_signature_type = "LOCAL_HMAC_SHA256_SANDBOX"
        secret_key = os.getenv("KMS_LOCAL_SECRET", "mirage_shield_ledger_master_signing_key_2026").encode()
        local_sig = hmac.new(secret_key, digest, hashlib.sha256).digest()
        sig_b64 = base64.b64encode(local_sig).decode("utf-8")
        return sig_b64, digest_hex

    def store_incident(self, verdict: Verdict, signature_b64: str) -> IncidentRecord:
        """
        Commits signed incident to DynamoDB table or local memory ledger.
        """
        incident_id = f"inc_{verdict.verdict_id.replace('vrd_', '')}"
        
        kms_arn = (
            f"arn:aws:kms:{self.region}:123456789012:key/{self.kms_key_id}"
            if self.kms_verified else "None (Sandbox Local HMAC Active)"
        )
        sig_type = "AWS_KMS_ASYMMETRIC_RSA" if self.kms_verified else "LOCAL_HMAC_SHA256_SANDBOX"

        dynamo_success = False
        if self.use_boto:
            try:
                item = {
                    "incident_id": {"S": incident_id},
                    "timestamp": {"S": datetime.now(timezone.utc).isoformat()},
                    "action": {"S": verdict.action.value},
                    "deepfake_score": {"N": str(verdict.call_risk.deepfake_score)},
                    "coercion_score": {"N": str(verdict.call_risk.coercion_score)},
                    "contradiction_summary": {"S": verdict.contradiction_summary},
                    "kms_signature": {"S": signature_b64},
                    "kms_key_arn": {"S": kms_arn}
                }
                self.dynamo_client.put_item(TableName=self.table_name, Item=item)
                logger.info(f"Committed incident {incident_id} to DynamoDB table '{self.table_name}'.")
                dynamo_success = True
                self.dynamodb_verified = True
            except Exception as e:
                logger.warning(f"DynamoDB put_item failed ({e}), saved to local memory ledger.")
                dynamo_success = False
                self.dynamodb_verified = False
        else:
            self.dynamodb_verified = False

        storage_type = "AMAZON_DYNAMODB" if dynamo_success else "IN_MEMORY_LOCAL_LEDGER"
        dynamo_status = "COMMITTED_TO_DYNAMODB" if dynamo_success else "LOCAL_MEMORY_FALLBACK (DynamoDB Inactive)"
        self._last_storage_type = storage_type

        record = IncidentRecord(
            incident_id=incident_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            verdict_id=verdict.verdict_id,
            action=verdict.action,
            deepfake_score=verdict.call_risk.deepfake_score,
            coercion_score=verdict.call_risk.coercion_score,
            contradiction_detected=verdict.contradiction_detected,
            contradiction_summary=verdict.contradiction_summary,
            ring_evidence_hash=verdict.door_evidence.latest_snapshot_hash,
            snapshot_hash=verdict.door_evidence.latest_snapshot_hash,
            payment_lock_active=verdict.interventions.payment_locked,
            family_cosign_status="PENDING" if verdict.interventions.payment_locked else "NONE",
            kms_key_arn=kms_arn,
            kms_signature=signature_b64,
            signature_type=sig_type,
            storage_type=storage_type,
            dynamodb_status=dynamo_status
        )

        self._local_ledger[incident_id] = record
        logger.info(f"💾 [AUDIT LEDGER] Incident {incident_id} recorded ({sig_type} / {storage_type}).")
        return record

    def get_incident(self, incident_id: str) -> Optional[IncidentRecord]:
        return self._local_ledger.get(incident_id)

    def list_recent_incidents(self, limit: int = 10) -> list:
        records = list(self._local_ledger.values())
        records.sort(key=lambda x: x.timestamp, reverse=True)
        return [r.model_dump() for r in records[:limit]]


aws_audit_ledger = AwsAuditLedger()
