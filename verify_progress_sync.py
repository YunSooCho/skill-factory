import os
import re
import sys
import io

# Force UTF-8 output to avoid CP932 encoding errors on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_sync():
    repo_dir = "repo"
    progress_dir = "progress"
    
    # 1. Get all directories in repo/
    if not os.path.exists(repo_dir):
        print(f"Error: Directory '{repo_dir}' not found.")
        return
        
    repo_services = set(os.listdir(repo_dir))
    
    # 2. Get all services inside progress markdown files
    md_services = set()
    completed_md_services = set()
    incomplete_md_services = set()
    
    if not os.path.exists(progress_dir):
        print(f"Error: Directory '{progress_dir}' not found.")
        return
        
    for filename in os.listdir(progress_dir):
        if not filename.endswith(".md"):
            continue
            
        file_path = os.path.join(progress_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            # Look for lines like "- [x] service_name" or "- [ ] service_name"
            # Note: We need to handle potential markdown links or extra spaces
            match = re.search(r'- \[([xX\s])\]\s+(?:\[(.*?)\]\(.*?\)|(.*?))\s*(?:$|<)', line)
            
            if match:
                is_checked = match.group(1).lower() == 'x'
                # Service name is either in the link text (group 2) or plain text (group 3)
                service_name = match.group(2) if match.group(2) else match.group(3)
                
                if service_name:
                    service_name = service_name.strip()
                    md_services.add(service_name)
                    if is_checked:
                        completed_md_services.add(service_name)
                    else:
                        incomplete_md_services.add(service_name)

    print("\n" + "="*50)
    print(f"REPORT: Service Integration Status")
    print("="*50)
    
    print(f"\nTotal services in progress MD files: {len(md_services)}")
    print(f"Marked as completed in MD: {len(completed_md_services)}")
    print(f"Marked as incomplete in MD: {len(incomplete_md_services)}")
    
    print(f"\nTotal service folders in 'repo/': {len(repo_services)}")
    
    md_not_in_repo = md_services - repo_services
    repo_not_in_md = repo_services - md_services
    
    print(f"\nWARNING: {len(md_not_in_repo)} services listed in MD but missing a folder in 'repo/':")
    for svc in sorted(md_not_in_repo):
        status = "(marked complete)" if svc in completed_md_services else "(incomplete)"
        print(f"   - {svc} {status}")
        
    print(f"\nWARNING: {len(repo_not_in_md)} folders in 'repo/' but missing from progress MD files (first 20 displayed):")
    for svc in sorted(list(repo_not_in_md))[:20]:
        print(f"   - {svc}")
    if len(repo_not_in_md) > 20:
        print(f"   ... and {len(repo_not_in_md) - 20} more.")

    uncompleted = len(incomplete_md_services)
    missing_folders = len(md_not_in_repo)
    
    print("\n" + "="*50)
    if uncompleted == 0 and missing_folders == 0:
        print("SUCCESS: All services in progress files are complete AND have matching repo folders!")
    else:
        print("CONCLUSION: Integration work is NOT completely finished.")
        if uncompleted > 0:
            print(f"   - Need to check off {uncompleted} services in MD files.")
        if missing_folders > 0:
            print(f"   - Need to create/rename folders for {missing_folders} services.")
    print("="*50 + "\n")

if __name__ == "__main__":
    check_sync()
