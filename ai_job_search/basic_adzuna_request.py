import requests
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")
country = "us"

# the minimum code to make a request to the Adzuna API
response = requests.get(
    f"https://api.adzuna.com/v1/api/jobs/{country}/categories",
    headers={"Accept": "application/json"},
    params={"app_id": api_id, "app_key": api_key},
)

print(response)