import os
import shutil
import glob
import re

REPO_DIR = "repo"
PROGRESS_DIR = "progress"

def get_category_mappings():
    """Reads progress markdown files to map service names to their new category folder name."""
    mappings = {}
    categories = []
    
    if not os.path.exists(PROGRESS_DIR):
        print(f"Directory {PROGRESS_DIR} does not exist.")
        return mappings, categories

    for filename in os.listdir(PROGRESS_DIR):
        if not filename.endswith(".md"):
            continue
            
        # extract like "01_Marketing" from "01_마케팅_Marketing.md"
        match = re.match(r"^(\d{2})_.*_([a-zA-Z0-9\-]+)\.md$", filename)
        if match:
            category_num = match.group(1)
            category_name = match.group(2)
            cat_folder = f"{category_num}_{category_name}"
        else:
            cat_folder = filename.replace(".md", "")
            
        categories.append(cat_folder)
        
        filepath = os.path.join(PROGRESS_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("- [x]") or line.startswith("- [ ]"):
                    service_match = re.search(r"- \[[x ]\] (.+)", line)
                    if service_match:
                        service_name = service_match.group(1).strip()
                        mappings[service_name] = cat_folder
                        # also support lower case or different hyphen rules just in case
                        mappings[service_name.lower()] = cat_folder
                        mappings[service_name.replace(" ", "-").lower()] = cat_folder

    return mappings, categories

def has_tests(service_path):
    """Checks if a service folder has tests implemented."""
    test_files = glob.glob(os.path.join(service_path, "test_*.py"))
    test_dir = os.path.join(service_path, "tests")
    
    if test_files:
        return True
    if os.path.isdir(test_dir) and any(f.endswith(".py") for f in os.listdir(test_dir)):
        return True
        
    return False

def run_restructure():
    mappings, categories = get_category_mappings()
    if not mappings:
        print("No mappings found!")
        return

    print(f"Loaded mappings for {len(mappings)} specific formatted names into {len(categories)} categories.")
    
    # Create the base category directories
    for cat in categories:
        verified_path = os.path.join(REPO_DIR, cat, "verified")
        developed_path = os.path.join(REPO_DIR, cat, "developed")
        os.makedirs(verified_path, exist_ok=True)
        os.makedirs(developed_path, exist_ok=True)

    moved_count = 0
    not_matched = []

    # Iterate through existing repo folders
    for service_dir in os.listdir(REPO_DIR):
        service_path = os.path.join(REPO_DIR, service_dir)
        
        # Skip if it's not a directory or if it's one of our new category folders
        if not os.path.isdir(service_path) or service_dir in categories:
            continue

        # Try to find the target category
        target_cat = None
        if service_dir in mappings:
            target_cat = mappings[service_dir]
        elif service_dir.replace("-", "_") in mappings:
            target_cat = mappings[service_dir.replace("-", "_")]
        elif service_dir.lower() in mappings:
            target_cat = mappings[service_dir.lower()]
        else:
            # try fuzzy matching against keys
            for key, val in mappings.items():
                if key.lower().replace("-", "") == service_dir.lower().replace("-", "").replace("_",""):
                    target_cat = val
                    break

        if target_cat:
            # determine status
            status = "verified" if has_tests(service_path) else "developed"
            dest_dir = os.path.join(REPO_DIR, target_cat, status, service_dir)
            
            try:
                shutil.move(service_path, dest_dir)
                moved_count += 1
                if moved_count % 50 == 0:
                    print(f"Moved {moved_count} services...")
            except Exception as e:
                print(f"Error moving {service_dir}: {e}")
        else:
            not_matched.append(service_dir)

    print(f"\\nSuccessfully moved {moved_count} services.")
    if not_matched:
        print(f"Warning: {len(not_matched)} services were not found in the markdown mappings:")
        for nm in not_matched[:10]:
            print(f"  - {nm}")
        if len(not_matched) > 10: print(f"  ... and {len(not_matched)-10} more.")

if __name__ == "__main__":
    run_restructure()
