import json
from datetime import UTC, datetime
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import pandas as pd

os.chdir(os.path.dirname(os.path.abspath(__file__)))

df = pd.read_excel("portfolio_media/VEX_Volunteering.xlsx")
df['Event'] = df.apply(lambda row: f'<a href="{row["Link"]}">{row["Event"]}</a>', axis=1)
df = df.drop(columns=["Link", "Setup"])
vex_volunteering_html = df.to_html(escape=False, index=False)

# Load JSON data
with Path("portfolio.json").open(encoding="utf-8") as f:
    data = json.load(f)

# Add any extra context if needed
data["current_year"] = datetime.now(tz=UTC).year
data["volunteer_experience"][0]["summary"] = vex_volunteering_html

if "social_links" in data:
    for link in data["social_links"]:
        if link.get("svg_path"):
            with Path(link["svg_path"]).open(encoding="utf-8") as svg_file:
                link["svg_data"] = svg_file.read()

# Set up Jinja environment
env = Environment(loader=FileSystemLoader("."), autoescape=True, cache_size=0)
index_template = env.get_template("index_template.html")
resume_template = env.get_template("resume_template.html")

# Render the template with the data
html_output = index_template.render(**data)
resume_output = resume_template.render(**data)

# Write the output to an HTML file
with Path("index.html").open("w", encoding="utf-8") as f:
    f.write(html_output)

print("HTML file generated successfully: " + str(Path("index.html").resolve()))

# with Path("resume.html").open("w", encoding="utf-8") as f:
#     f.write(resume_output)