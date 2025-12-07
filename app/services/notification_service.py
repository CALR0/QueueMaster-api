from app.utils.notifications_mock import send_notification


def notify_client(to: str, subject: str, message: str, channel: str = "email") -> dict:
    return send_notification(to=to, subject=subject, message=message, channel=channel)
