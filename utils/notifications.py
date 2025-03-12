import requests

def send_slack_notification(webhook_url, message):
    payload = {"text": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        print(f"⚠️ Slack Error: {response.text}")

def send_discord_notification(webhook_url, message):
    payload = {"content": message}
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 204:  # Discord returns 204 No Content on success
        print(f"⚠️ Discord Error: {response.text}")
