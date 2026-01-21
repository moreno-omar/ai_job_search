# To test connection between app and adzuna API
import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

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

# Drop metadata-only and unnecessary columns
columns_to_drop = [col for col in df.columns if col.endswith("__CLASS__")]
columns_to_drop.extend(["latitude", "adref", "category_label", "category_tag", "location_area"])
df = df.drop(columns=columns_to_drop, errors="ignore")

# Reindex to rearrange columns: company first, then title, salary_min,
# middle columns, then redirect_url and description at end
cols = df.columns.tolist()
cols.remove("company_display_name")
cols.remove("title")
cols.remove("salary_min")
cols.remove("redirect_url")
cols.remove("description")

new_order = ["company_display_name", "title", "salary_min"] + cols + ["redirect_url", "description"]
df = df.reindex(columns=new_order)

# Save flattened DataFrame to CSV
output_path = "jobs_flat.csv"
df.to_csv(output_path, index=False)
print(f"Wrote {len(df)} rows to {output_path}")

# Render template using existing DataFrame
jobs = df.to_dict("records")
columns = df.columns.tolist()

# Setup Jinja environment
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("jobs_table.html")

# Render to string
html_output = template.render(
    jobs=jobs,
    columns=columns,
    job_count=len(jobs),
    generation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)

# Write to file
html_file = "jobs_output.html"
with open(html_file, "w", encoding="utf-8") as f:
    f.write(html_output)

print(f"HTML file created: {html_file}")
