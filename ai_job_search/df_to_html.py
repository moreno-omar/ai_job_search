from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import os

def df_to_html(df):
    # Render template using existing DataFrame
    jobs = df.to_dict("records")
    columns = df.columns.tolist()

    # Setup Jinja environment with absolute path to templates
    # Get the directory containing this file, then go up one level to reach project root
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(os.path.dirname(current_dir), "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))
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