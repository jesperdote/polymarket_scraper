import json
import os
from utils.api import fetch_market_data
from utils.slack import send_slack_notification

# Load Slack webhook URL from file
WEBHOOK_FILE = "webhook.txt"
SLACK_WEBHOOK_URL = None

if os.path.exists(WEBHOOK_FILE):
    with open(WEBHOOK_FILE, "r") as f:
        SLACK_WEBHOOK_URL = f.read().strip()
else:
    print("⚠️ Warning: No Slack webhook file found. Notifications are disabled.")

# Read slugs from a text file
with open("markets.txt", "r") as file:
    slugs = [line.strip() for line in file if line.strip()]

for slug in slugs:
    data = fetch_market_data(slug)

    if data:
        outcomes = json.loads(data[0].get("outcomes", "[]"))
        prices = json.loads(data[0].get("outcomePrices", "[]"))

        print(f"\nEvent: {slug}")

        alert_outcomes = []  # Store outcomes above 0.80

        for outcome, price in zip(outcomes, prices):
            print(f"{outcome} = {price}")
            if float(price) > 0.10:
                alert_outcomes.append(f"*{outcome}* is at *{price}*")

        # Send Slack alert only if any outcome is above 0.80
        if alert_outcomes and SLACK_WEBHOOK_URL:
            market_url = f"https://polymarket.com/market/{slug}"
            link = f"<{market_url}|{slug}>"
            message = f"📈 *Trading Signal:* {link} \nMarket activity is rising!\n" + "\n".join(alert_outcomes)
            send_slack_notification(SLACK_WEBHOOK_URL, message)

    else:
        print(f"\nEvent: {slug} - No data found.")
