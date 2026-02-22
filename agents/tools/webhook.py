# agents/tools/webhook.py

import requests
import os

WEBHOOK_URL = "https://n8n.srv1403775.hstgr.cloud/webhook/pharmacy-events"

def trigger_admin_alert(event_type: str, payload: dict):

    if not WEBHOOK_URL:
        return {"status": "no_webhook_configured"}

    try:
        # Merge event_type into main body for easier n8n mapping
        data = {
            "event_type": event_type,
            **payload
        }

        response = requests.post(
            WEBHOOK_URL,
            json=data,
            timeout=5
        )

        return {"status": "sent", "code": response.status_code}

    except Exception as e:
        return {"status": "failed", "error": str(e)}