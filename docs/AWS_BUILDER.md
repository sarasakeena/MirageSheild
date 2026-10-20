# MIRAGE-SHIELD AWS Builder Challenge Submission

> **AWS Builder Track: Service Architecture & Implementation Guide**
> How MIRAGE-SHIELD leverages Amazon Web Services to build an enterprise-grade, cryptographically tamper-evident living room scam defense system.

---

## AWS Services Leveraged

### 1. Amazon Bedrock & Strands Agents SDK
- **Role**: Core Cognitive Reasoning Brain.
- **Model Used**: `anthropic.claude-3-haiku-20240307-v1:0` (fallback: `amazon.titan-text-express-v1`).
- **Implementation**:
  - The agent orchestrates 5 primary tools: `get_door_evidence`, `score_call`, `lock_payments`, `notify_family`, and `trigger_tv_alert`.
  - It cross-examines the caller's spoken claims (extracted via regex/NLP) against real-time Ring Doorbell sensor logs.
  - Generates structured, confidence-weighted verdicts (`SAFE`, `WARN`, `INTERVENE`).

### 2. AWS Key Management Service (AWS KMS)
- **Role**: Cryptographic Chain of Custody & Incident Integrity.
- **Key Spec**: Asymmetric RSA Key Pair (`RSA_2048`, `RSASSA_PKCS1_V1_5_SHA_256`).
- **Implementation**:
  - Every scam detection event is digested using SHA-256 (combining the call transcript, deepfake score, Ring sensor event hash, and front door snapshot SHA256).
  - The digest is submitted to KMS via `kms.sign()`.
  - The resulting cryptographic signature is permanently bound to the incident record, guaranteeing that neither the victim, family, nor malicious actors can alter the forensic evidence presented to the National Cyber Crime Portal (1930) or law enforcement.

### 3. Amazon DynamoDB
- **Role**: Immutable Forensic Incident Ledger.
- **Table Name**: `mirage_shield_incidents`.
- **Partition Key**: `incident_id` (String).
- **Sort Key**: `timestamp` (ISO-8601 String).
- **Implementation**:
  - Stores the full audit trail: verdict action, confidence scores, contradiction text, Ring snapshot hash, KMS signature, and family co-sign release history.
  - Supports Point-In-Time Recovery (PITR) for forensic integrity.

### 4. Amazon Transcribe
- **Role**: Live Audio Stream Speech-to-Text.
- **Implementation**:
  - Transcribes live incoming call audio chunks into timestamped text.
  - Transcripts feed into the Coercion Classifier to detect extortion vocabulary, fake arrest warrants, and isolation demands.

### 5. AWS Lambda & AgentCore Runtime Architecture
- **Role**: Serverless Event-Driven Defense Engine.
- **Architecture**:
  - Ring webhooks trigger API Gateway $\rightarrow$ Lambda execution within 5 seconds.
  - Payment lock state is maintained with sub-millisecond DynamoDB read/writes.
  - Enables cost-efficient living room security that scales to zero when no calls are active.

---

## AWS Architecture Diagram

```
[ Ring Partner API Webhook ] ──▶ [ Amazon API Gateway ]
                                         │
                                         ▼
                               [ AWS Lambda / AgentCore ]
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
           [ Amazon Bedrock ]      [ AWS KMS ]      [ Amazon DynamoDB ]
          (Cognitive Reasoning)  (Digital Signature)   (Incident Ledger)
```
