import re
import json

with open("yoom_apps.html", "r", encoding="utf-8") as f:
    html = f.read()

# Try to find Next.js data
match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html)
if match:
    data = json.loads(match.group(1))
    print("Found NEXT_DATA")
    with open("yoom_next_data.json", "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)
else:
    print("NEXT_DATA not found. Looking for other JSON objects or structured data.")
    
    # Maybe try to find window.__NUXT__ or something similar if it's Nuxt
    nuxt_match = re.search(r'window\.__NUXT__=(.*?);</script>', html)
    if nuxt_match:
        print("Found NUXT data")
        
    # Or just extract plain text or URLs
    links = re.findall(r'href="([^"]*/apps/[^"]+)"[^>]*>(.*?)</a>', html)
    print(f"Found {len(links)} links")
    for link in links[:5]:
        print(link)
