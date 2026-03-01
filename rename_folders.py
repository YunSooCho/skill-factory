import os
import re
import difflib

repo_dir = r"e:\skill-factory\repo"
progress_dir = r"e:\skill-factory\progress"

def normalize_name(name):
    # Remove hyphens and underscores for comparison
    return re.sub(r'[-_]', '', name.lower())

def main():
    if not os.path.exists(repo_dir) or not os.path.exists(progress_dir):
        print("Directory not found")
        return

    # Load all repo folders
    repo_folders = [f for f in os.listdir(repo_dir) if os.path.isdir(os.path.join(repo_dir, f))]
    repo_lower_map = {f.lower(): f for f in repo_folders}
    repo_normalized_map = {normalize_name(f): f for f in repo_folders}

    # Extract all marked [ ] services
    unchecked_services = []
    
    for filename in os.listdir(progress_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(progress_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            match = re.match(r'^\s*-\s*\[\s\]\s*(.+)$', line)
            if match:
                service_name = match.group(1).strip()
                unchecked_services.append(service_name)
    
    # Try to find matches and rename
    rename_count = 0
    for service_name in unchecked_services:
        lower_s = service_name.lower()
        norm_s = normalize_name(service_name)
        
        target_folder = None
        
        # Exact match lowercase (already should have been caught by earlier script, but double checking)
        if lower_s in repo_lower_map:
            target_folder = repo_lower_map[lower_s]
        # Match normalized
        elif norm_s in repo_normalized_map:
            target_folder = repo_normalized_map[norm_s]
        else:
            # Only rely on normalization to match differing symbols
            pass
                
        if target_folder and target_folder != service_name:
            old_path = os.path.join(repo_dir, target_folder)
            new_path = os.path.join(repo_dir, service_name)
            
            # Additional check to ensure case-sensitive rename doesn't fail on Windows
            if old_path.lower() == new_path.lower():
                temp_path = os.path.join(repo_dir, target_folder + "_TEMP")
                os.rename(old_path, temp_path)
                os.rename(temp_path, new_path)
            else:
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    
            print(f"Renamed: {target_folder} -> {service_name}")
            
            # update maps
            if target_folder in repo_folders:
                repo_folders.remove(target_folder)
                del repo_lower_map[target_folder.lower()]
                del repo_normalized_map[normalize_name(target_folder)]
            
            repo_folders.append(service_name)
            repo_lower_map[service_name.lower()] = service_name
            repo_normalized_map[normalize_name(service_name)] = service_name
            rename_count += 1
            
    print(f"Total renamed folders: {rename_count}")

if __name__ == "__main__":
    main()
