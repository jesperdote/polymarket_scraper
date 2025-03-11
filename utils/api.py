import requests

API_URL = "https://gamma-api.polymarket.com/markets"

def fetch_market_data(slug):
    """Fetch market data from the Polymarket API based on slug."""
    params = {"slug": slug, "closed": "false"}
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {slug}: {e}")
        return None
