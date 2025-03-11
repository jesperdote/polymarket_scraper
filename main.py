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

        alert_outcomes = []  # Store "No" outcomes below 0.50
        yes_price = None  # Track "Yes" price
        no_price = None  # Track "No" price

        for outcome, price in zip(outcomes, prices):
            if outcome.lower() == "yes":
                yes_price = price  # Store "Yes" price
            elif outcome.lower() == "no":
                no_price = price  # Store "No" price
                print(f"{outcome} = {price}")
                if float(price) > 0.80:
                    alert_outcomes.append(f"*No* is at {price}")

        # Display the "Yes" price
        if yes_price:
            print(f"Yes = {yes_price}")

        # Send Slack alert only if "No" outcome is below 0.50
        if alert_outcomes and SLACK_WEBHOOK_URL:
            market_url = f"https://polymarket.com/market/{slug}"
            link = f"<{market_url}|{slug}>"
            message = f"📈 *Trading Signal:* {link} \nMarket activity is rising!\n" + "\n".join(alert_outcomes) + f"\n*Yes* is at {yes_price}"
            send_slack_notification(SLACK_WEBHOOK_URL, message)

    else:
        print(f"\nEvent: {slug} - No data found.")


