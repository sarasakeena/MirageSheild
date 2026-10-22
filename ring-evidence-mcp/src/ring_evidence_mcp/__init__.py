"""
ring-evidence-mcp: Model Context Protocol (MCP) server for Ring Doorbell Physical Evidence.

Exposes physical door & porch sensor telemetry to LLM reasoning agents (Claude, Bedrock, GPT-4, etc.)
to verify real-world claims and prevent digital arrest extortion scams.
"""

__version__ = "0.1.0"
__author__ = "MIRAGE-SHIELD Open Source Contributors"
__license__ = "MIT"

from .server import mcp, get_door_evidence, verify_porch_claim

__all__ = ["mcp", "get_door_evidence", "verify_porch_claim"]
