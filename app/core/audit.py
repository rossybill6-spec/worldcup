"""
Audit logging utilities for tracking admin and system actions.
"""

from typing import Optional, Dict, Any
from datetime import datetime
import json


async def log_audit_event(
    action: str,
    performed_by: str,
    target_type: str,
    target_id: str,
    details: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    before_value: Optional[Dict[str, Any]] = None,
    after_value: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Log an audit event.
    """
    audit_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "performed_by": performed_by,
        "target_type": target_type,
        "target_id": target_id,
        "details": details or {},
        "ip_address": ip_address,
        "before": before_value,
        "after": after_value,
    }
    print(f"AUDIT: {json.dumps(audit_entry, default=str)}")
