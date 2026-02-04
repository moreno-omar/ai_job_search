import requests
from dotenv import load_dotenv

import json
import os

load_dotenv()

api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

def fetch_jobs(job_type: str = "engineering-jobs", key_words: str = "software", country: str = "us", page: int = 1):


    response = requests.get(
        f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
        headers={"Accept": "application/json"},
        params={
            "app_id": api_id,
            "app_key": api_key,
            "category": job_type,
            "title_only": key_words,
            "results_per_page": 100,
            "max_days_old": 21,
        },
    )
    
    response.raise_for_status()  # Raises an error for 4xx/5xx responses
    return response