"""Simulated notification sender.

In reality you'd integrate with email/SMS/push providers. This mock prints/logs.
"""
import logging

logger = logging.getLogger("notifications")


def send_notification(to: str, subject: str, message: str, channel: str = "email") -> dict:
    # Simulate sending
    payload = {"to": to, "subject": subject, "message": message, "channel": channel}
    logger.info("Mock send: %s", payload)
    # Return a simulated response
    return {"status": "sent", "detail": payload}
