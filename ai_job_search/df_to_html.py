from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def df_to_html(df):
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