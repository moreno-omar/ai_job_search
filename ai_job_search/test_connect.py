# To test connection between app and adzuna API
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

response = requests.get(
    "https://api.adzuna.com/v1/api/jobs",
    headers={"Accept": "application/json"}
    )

# If response.json() returns a dict/list:
with open('response.json', 'w') as f:
    json.dump(response.json(), f, indent=2)