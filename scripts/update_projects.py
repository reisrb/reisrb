import os
import re
import requests

USERNAME = "reisrb"
TOKEN = os.environ.get("GITHUB_TOKEN")
EXCLUDE = {USERNAME}  # exclude the profile repo itself

headers = {"Authorization": f"Bearer {TOKEN}", "Accept": "application/vnd.github+json"}

resp = requests.get(
    f"https://api.github.com/users/{USERNAME}/repos",
    headers=headers,
    params={"sort": "updated", "per_page": 100},
)
repos = [r for r in resp.json() if not r["fork"] and r["name"] not in EXCLUDE]
repos.sort(key=lambda r: r["stargazers_count"], reverse=True)
top = repos[:6]

rows = ["| Repo | Language | Stars |", "|------|----------|-------|"]
for r in top:
    name = r["name"]
    url = r["html_url"]
    lang = r["language"] or "—"
    stars = f"⭐ {r['stargazers_count']}" if r["stargazers_count"] else "—"
    desc = (r["description"] or "").replace("|", "\\|")
    rows.append(f"| [{name}]({url}) | {lang} | {stars} |")
    if desc:
        rows.append(f"| *{desc}* | | |")

table = "\n".join(rows)

readme_path = "README.md"
with open(readme_path) as f:
    content = f.read()

updated = re.sub(
    r"<!-- PROJECTS:START -->.*?<!-- PROJECTS:END -->",
    f"<!-- PROJECTS:START -->\n{table}\n<!-- PROJECTS:END -->",
    content,
    flags=re.DOTALL,
)

with open(readme_path, "w") as f:
    f.write(updated)

print("README updated.")
