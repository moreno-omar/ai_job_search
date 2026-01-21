import requests

# the minimum code to make a request to the Adzuna API
response = requests.get(
    f"https://api.adzuna.com/v1/api/jobs/{country}/categories",
    headers={"Accept": "application/json"},
    params={"app_id": api_id, "app_key": api_key},