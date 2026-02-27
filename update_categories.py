import os
import re
import glob

# 1. Parse HTML to create app -> category mapping
html_path = "yoom_apps.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Extract <a id="Category" href="/apps/slug">
matches = re.findall(r'<a id="([^"]+)"\s*href="/apps/([^"]+)"', html)
mapping = {}
for category, slug in matches:
    mapping[slug] = category

print(f"Extracted {len(mapping)} app-to-category mappings from HTML.")

# 2. Iterate through markdown files in yoom-apps directory
apps_dir = "yoom-apps"
md_files = glob.glob(os.path.join(apps_dir, "*.md"))

updated_count = 0
not_found_count = 0
error_count = 0

for filepath in md_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find the URL to extract the slug
        # e.g., - **URL:** https://lp.yoom.fun/apps/zoom
        url_match = re.search(r'-\s*\*\*URL:\*\*\s*https://lp\.yoom\.fun/apps/([^\s]+)', content)
        
        if not url_match:
            # Maybe the URL is different or missing
            # Try to get it from the file name
            basename = os.path.basename(filepath)
            slug, _ = os.path.splitext(basename)
            print(f"[{basename}] Warning: Could not find URL in content. Using filename '{slug}' as slug.")
        else:
            slug = url_match.group(1)
            
        if slug in mapping:
            new_cat = mapping[slug]
            # Find and replace the category line
            # Default line looks like: - **カテゴリー:** 業務一般
            # It might have spaces or different names.
            # We will use regex to replace it.
            
            # Using re.sub to find category line
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
                # Content didn't change (maybe category was already correct)
                # or the line wasn't found (maybe the markdown is formatted differently)
                if not re.search(r'-\s*\*\*カテゴリー:\*\*', content):
                    print(f"[{os.path.basename(filepath)}] Warning: Could not find Category line to replace.")
                else:
                    # Category was already up to date
                    pass 
        else:
            not_found_count += 1
            print(f"[{os.path.basename(filepath)}] Slug '{slug}' not found in the Yoom HTML mapping.")
            
    except Exception as e:
        error_count += 1
        print(f"[{os.path.basename(filepath)}] Error processing file: {e}")

print(f"Finished. Updated {updated_count} files. Not found: {not_found_count}. Errors: {error_count}.")
