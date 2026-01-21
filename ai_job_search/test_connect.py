# To test connection between app and adzuna API
import json
import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv("API_ID")
api_key = os.getenv("API_KEY")

# strings to replace in the URL
country = "us"
page = 1

response = requests.get(
    f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}",
    headers={"Accept": "application/json"},
    params={
        "app_id": api_id,
        "app_key": api_key,
        "category": "engineering-jobs",
        "title_only": "software",
        "results_per_page": 100,
        "max_days_old": 21,
    },
)

data = response.json()

# Persist raw payload for debugging
with open("response.json", "w") as f:
    json.dump(data, f, indent=2)

# Extract results array and normalize into DataFrame
results = data.get("results", [])
df = pd.json_normalize(results, sep="_")

# Drop metadata-only columns
columns_to_drop = [col for col in df.columns if col.endswith("__CLASS__")]
df = df.drop(columns=columns_to_drop, errors="ignore")

# Split location_area list into separate columns
if "location_area" in df.columns:
    area_levels = ("country", "state", "county", "city")
    for idx, level in enumerate(area_levels):
        df[f"location_{level}"] = df["location_area"].apply(
            lambda x: x[idx] if isinstance(x, list) and len(x) > idx else None
        )

# Save flattened DataFrame to CSV
output_path = "jobs_flat.csv"
df.to_csv(output_path, index=False)
print(f"Wrote {len(df)} rows to {output_path}")