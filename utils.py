import requests
import os
import logging
from datetime import datetime

def search_unclaimed_funds(name):
    logging.debug(f"Searching for unclaimed funds for {name}")
    api_url = "https://api.missingmoney.com/v1/search"
    headers = {"Authorization": f"Bearer {os.getenv('MISSING_MONEY_API_KEY')}", "Content-Type": "application/json"}
    payload = {"firstName": name.split()[0], "lastName": name.split()[-1], "state": "ALL"}

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return {"results": data.get("properties", [])}
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        return {"results": []}
