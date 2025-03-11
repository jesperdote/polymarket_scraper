import requests
import json

def send_slack_notification(webhook_url, message):
    """Send a Slack notification with the given message."""
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        print("✅ Slack notification sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error sending Slack notification: {e}")
