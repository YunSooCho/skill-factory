import os
import re
import time
from deep_translator import GoogleTranslator

KO_PATTERN = re.compile(r'[가-힣]')

# Markdown links, URLs, and code blocks preservation logic
MARKDOWN_LINK_PATTERN = re.compile(r'(\[[^\]]+\]\([^\)]+\))')
URL_PATTERN = re.compile(r'(https?://[^\s]+)')

def contains_korean(text):
    return bool(KO_PATTERN.search(text))

def get_files_with_korean(root_dir='.'):
    matched_files = []
    for root, dirs, files in os.walk(root_dir):
        if '/.' in root or '\\.' in root or 'node_modules' in root or '__pycache__' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            # Skip non-text extensions or translation script
            if file.endswith(('.png', '.pyc', '.jpg', '.zip', '.jar')) or file in ('translate_project.py', 'translate_project_free.py'):
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        if contains_korean(line):
                            matched_files.append(filepath)
                            break
            except Exception:
                pass
    return matched_files

def translate_line(line, translator):
    if not contains_korean(line):
        return line
    
    # We will try to translate the whole line using Google Translate, 
    # but it might mess up markdown tables or links.
    # Preserve leading whitespace
    leading_whitespace = len(line) - len(line.lstrip())
    indent = line[:leading_whitespace]
    core_text = line[leading_whitespace:]
    
    urls = URL_PATTERN.findall(core_text)
    placeholders = []
    
    temp_line = core_text
    for i, url in enumerate(urls):
        placeholder = f"__URL_PLACEHOLDER_{i}__"
        placeholders.append((placeholder, url))
        temp_line = temp_line.replace(url, placeholder)
        
    try:
        translated_line = translator.translate(temp_line)
    except Exception as e:
        print(f"Error translating line: {e}")
        return line # return original on failure

    if translated_line is None:
        return line

    for placeholder, url in placeholders:
        translated_line = translated_line.replace(placeholder, url)
        
    # Match the trailing newline if original had it
    if line.endswith('\n') and not translated_line.endswith('\n'):
        translated_line += '\n'
        
    return indent + translated_line

def translate_file(filepath, translator):
    print(f"Translating: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_code_block = False
        
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                new_lines.append(line)
                continue
            
            if in_code_block:
                new_lines.append(line) # Do not translate code blocks usually
            else:
                new_lines.append(translate_line(line, translator))

        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print(f"Successfully translated: {filepath}")
        return True
    except Exception as e:
        print(f"Failed to translate {filepath}: {e}")
        return False

def main():
    print("Starting translation process using deep-translator (Google)...")
    translator = GoogleTranslator(source='ko', target='ja')
    
    files_to_translate = get_files_with_korean()
    print(f"Found {len(files_to_translate)} files containing Korean text.")

    success_count = 0
    
    for count, filepath in enumerate(files_to_translate):
        if translate_file(filepath, translator):
            success_count += 1
        
        time.sleep(0.5) # rate limit prevention
        
        if (count + 1) % 50 == 0:
            print(f"Progress: {count + 1} / {len(files_to_translate)} processed...")

    print(f"\nTranslation completed. Successfully translated {success_count}/{len(files_to_translate)} files.")

if __name__ == "__main__":
    main()
