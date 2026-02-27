import re
import os

with open("yoom_apps.html", "r", encoding="utf-8") as f:
    html = f.read()

# Try to find links like <a id="業務一般" href="/apps/zoom" class="app_item_link w-inline-block">
matches = re.findall(r'<a id="([^"]+)"\s*href="/apps/([^"]+)"', html)
mapping = {}
for category, slug in matches:
    mapping[slug] = category

print(f"Found {len(mapping)} app-category mappings.")
for k, v in list(mapping.items())[:5]:
    print(f"  {k}: {v}")

