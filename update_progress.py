import os
import re

repo_dir = r"e:\skill-factory\repo"
progress_dir = r"e:\skill-factory\progress"

def main():
    if not os.path.exists(repo_dir):
        print(f"Error: Repo directory not found: {repo_dir}")
        return
    if not os.path.exists(progress_dir):
        print(f"Error: Progress directory not found: {progress_dir}")
        return
        
    repo_services = set()
    for item in os.listdir(repo_dir):
        if os.path.isdir(os.path.join(repo_dir, item)):
            repo_services.add(item.lower())

    for filename in os.listdir(progress_dir):
        if not filename.endswith(".md"):
            continue
        filepath = os.path.join(progress_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if not lines:
            continue
            
        total_count = 0
        completed_count = 0
        
        new_lines = []
        header_line_index = -1
        
        for i, line in enumerate(lines):
            if line.startswith('#') and i == 0:
                header_line_index = i
                new_lines.append(line)
                continue
                
            match = re.match(r'^(\s*-\s*\[)([ xX]?)(\]\s*)(.+)$', line)
            if match:
                prefix = match.group(1)
                suffix = match.group(3)
                service_name_raw = match.group(4).strip()
                
                service_name_clean = service_name_raw.lower()
                
                total_count += 1
                if service_name_clean in repo_services:
                    completed_count += 1
                    new_line = prefix + "x" + suffix + service_name_raw + "\n"
                else:
                    new_line = prefix + " " + suffix + service_name_raw + "\n"
                    
                new_lines.append(new_line)
            else:
                new_lines.append(line)
                
        if header_line_index != -1:
            old_header = new_lines[header_line_index]
            title_match = re.search(r'^(#\s+.*?)(?:\s*\(\d+/\d+\))?\s*$', old_header)
            if title_match:
                base_title = title_match.group(1).strip()
                new_lines[header_line_index] = f"{base_title} ({completed_count}/{total_count})\n"

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print(f"Updated {filename}: ({completed_count}/{total_count}) completed.".encode('utf-8').decode('cp932', 'ignore'))
            
    print("Progress update completed (進捗更新完了)")

if __name__ == "__main__":
    main()
