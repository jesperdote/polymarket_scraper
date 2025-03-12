import json
import os
from utils.api import fetch_market_data
from utils.notifications import send_slack_notification, send_discord_notification

# Load webhook URLs from file
WEBHOOK_FILE = "webhook.txt"
SLACK_WEBHOOK_URL = None
DISCORD_WEBHOOK_URL = None

if os.path.exists(WEBHOOK_FILE):
    with open(WEBHOOK_FILE, "r") as f:
        lines = f.readlines()
        if len(lines) > 0:
            SLACK_WEBHOOK_URL = lines[0].strip()
        if len(lines) > 1:
            DISCORD_WEBHOOK_URL = lines[1].strip()
else:
    print("⚠️ Warning: No webhook file found. Notifications are disabled.")

# Read slugs from a text file
with open("markets.txt", "r") as file:
    slugs = [line.strip() for line in file if line.strip()]

for slug in slugs:
    data = fetch_market_data(slug)

    if data:
        outcomes = json.loads(data[0].get("outcomes", "[]"))
        prices = json.loads(data[0].get("outcomePrices", "[]"))
        print(f"\nEvent: {slug}")

        alert_outcomes = []  # Store "No" outcomes above 0.80
        yes_price = None  # Track "Yes" price
        no_price = None  # Track "No" price

        for outcome, price in zip(outcomes, prices):
            if outcome.lower() == "yes":
                yes_price = price  # Store "Yes" price
            elif outcome.lower() == "no":
                no_price = price  # Store "No" price
                print(f"{outcome} = {price}")
                if float(price) > 0.80:
                    alert_outcomes.append(f"*No* is at *{price}*")

        # Display the "Yes" price
        if yes_price:
            print(f"Yes = {yes_price}")

        # Send alert if "No" outcome is above 0.80
        if alert_outcomes:
            market_url = f"https://polymarket.com/market/{slug}"
            link = f"<{market_url}|{slug}>"  # Slack hyperlink format
            message = f"📈 *Market Alert:* {link}\n'No' is trending above 0.80!\n" + "\n".join(alert_outcomes) + f"\n*Yes* is at {yes_price}"

            if SLACK_WEBHOOK_URL:
                send_slack_notification(SLACK_WEBHOOK_URL, message)

            if DISCORD_WEBHOOK_URL:
                discord_message = f"📈 **Market Alert:** [{slug}]({market_url})\n'No' is trending above 0.80!\n" + "\n".join(alert_outcomes) + f"\n**Yes** is at {yes_price}"
                send_discord_notification(DISCORD_WEBHOOK_URL, discord_message)

    else:
        print(f"\nEvent: {slug} - No data found.")
