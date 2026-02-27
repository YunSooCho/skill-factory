import os
import re
import glob

html_path = "yoom_apps.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

matches = re.findall(r'<a id="([^"]+)"\s*href="/apps/([^"]+)"', html)
mapping = {}
for category, slug in matches:
    mapping[slug] = category

apps_dir = "yoom-apps"
md_files = glob.glob(os.path.join(apps_dir, "*.md"))

updated_count = 0
not_found_count = 0
already_correct_count = 0
no_category_line_count = 0

for filepath in md_files:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    url_match = re.search(r'-\s*\*\*URL:\*\*\s*https://lp\.yoom\.fun/apps/([^\s]+)', content)
    if url_match:
        slug = url_match.group(1)
        if slug in mapping:
            new_cat = mapping[slug]
            cat_match = re.search(r'-\s*\*\*カテゴリー:\*\*\s*(.*)', content)
            if cat_match:
                if cat_match.group(1).strip() == new_cat:
                    already_correct_count += 1
                else:
                    new_content = re.sub(
                        r'(-\s*\*\*カテゴリー:\*\*\s*)(.*)', 
                        rf'\g<1>{new_cat}', 
                        content
                    )
                    if new_content != content:
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        updated_count += 1
            else:
                no_category_line_count += 1
                print(f"[{os.path.basename(filepath)}] No category line found.")
        else:
            not_found_count += 1
            print(f"[{os.path.basename(filepath)}] Slug '{slug}' not found in mapping.")
    else:
        # no URL line found...?
        pass

print(f"Updated: {updated_count}, Already correct: {already_correct_count}, No line: {no_category_line_count}, Not in mapping: {not_found_count}")
