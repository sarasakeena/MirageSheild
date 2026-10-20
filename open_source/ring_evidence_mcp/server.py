"""
Ring Evidence MCP (Model Context Protocol) Server
An open-source MCP server allowing any AI agent to query Ring video doorbells
as a physical-world Evidence Oracle to verify real-world claims and sound alarms.
"""

import sys
import json
import logging
from typing import Dict, Any, List
from shared.schemas import DoorEvidence, DoorStatus
from ring_service.evidence import DoorEvidenceOracle
from ring_service.chime import ChimeAlertService

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("ring_evidence_mcp")


class RingEvidenceMcpServer:
    """
    Model Context Protocol (MCP) Server for Ring Doorbell Physical Evidence.
    Conforms to MCP JSON-RPC 2.0 tool definitions.
    """

    def __init__(self):
        self.oracle = DoorEvidenceOracle()
        self.chime = ChimeAlertService()

    def get_tools_manifest(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": "get_door_evidence",
                "description": (
                    "Inspects the physical front door via Ring Doorbell over a given time window (in hours). "
                    "Returns counts of humans, vehicles, packages, doorbell presses, and snapshot hash."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "window_hours": {
                            "type": "integer",
                            "description": "Number of past hours to inspect (default 6)",
                            "default": 6
                        },
                        "device_id": {
                            "type": "string",
                            "description": "Ring Doorbell device ID (optional)"
                        }
                    }
                }
            },
            {
                "name": "verify_physical_claim",
                "description": (
                    "Cross-examines a suspect's claim (e.g. 'police standing outside door', 'package seized') "
                    "against physical Ring sensor events. Detects whether the claim is a lie."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "claim_type": {
                            "type": "string",
                            "enum": ["officers_at_door", "package_delivered", "raid_underway"],
                            "description": "Type of physical claim to verify"
                        },
                        "window_hours": {
                            "type": "integer",
                            "default": 6
                        }
                    },
                    "required": ["claim_type"]
                }
            },
            {
                "name": "trigger_chime_alert",
                "description": "Sounds an urgent security audio slot on the living room Ring Chime device.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "audio_ref": {
                            "type": "string",
                            "description": "Audio slot reference identifier",
                            "default": "audio_ref_urgent_security_alert"
                        }
                    }
                }
            }
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "get_door_evidence":
            window = arguments.get("window_hours", 6)
            dev_id = arguments.get("device_id", "ring_doorbell_01_entrance")
            evidence = self.oracle.get_door_evidence(window_hours=window, device_id=dev_id)
            return evidence.model_dump()

        elif tool_name == "verify_physical_claim":
            claim_type = arguments.get("claim_type")
            window = arguments.get("window_hours", 6)
            evidence = self.oracle.get_door_evidence(window_hours=window)

            if claim_type in ("officers_at_door", "raid_underway"):
                is_contradiction = (evidence.human_events_count == 0)
                return {
                    "claim_verified": not is_contradiction,
                    "contradiction_detected": is_contradiction,
                    "door_status": evidence.door_status.value,
                    "human_events_detected": evidence.human_events_count,
                    "summary": (
                        "CONTRADICTION: Claim asserted officers outside door, but Ring verifies zero humans."
                        if is_contradiction else "Verified: Humans detected at entrance."
                    )
                }

            elif claim_type == "package_delivered":
                has_package = (evidence.package_events_count > 0)
                return {
                    "claim_verified": has_package,
                    "contradiction_detected": not has_package,
                    "packages_detected": evidence.package_events_count,
                    "summary": (
                        "VERIFIED: Package delivery detected by Ring camera."
                        if has_package else "CONTRADICTION: No package delivered on porch."
                    )
                }

        elif tool_name == "trigger_chime_alert":
            audio_ref = arguments.get("audio_ref", "audio_ref_urgent_security_alert")
            result = self.chime.alert_living_room(audio_ref=audio_ref)
            return result

        raise ValueError(f"Unknown tool: {tool_name}")

    def run_jsonrpc_loop(self):
        """Reads JSON-RPC from stdin and writes responses to stdout."""
        logger.info("Ring Evidence MCP Server running on stdio...")
        for line in sys.stdin:
            if not line.strip():
                continue
            try:
                request = json.loads(line)
                req_id = request.get("id")
                method = request.get("method")

                if method == "tools/list":
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"tools": self.get_tools_manifest()}
                    }
                elif method == "tools/call":
                    params = request.get("params", {})
                    tool_name = params.get("name")
                    args = params.get("arguments", {})
                    result = self.execute_tool(tool_name, args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {"content": [{"type": "text", "text": json.dumps(result)}]}
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "error": {"code": -32601, "message": f"Method {method} not found"}
                    }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32603, "message": str(e)}
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    server = RingEvidenceMcpServer()
    server.run_jsonrpc_loop()
