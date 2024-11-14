import os
import re

def parse_terraform_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Regular expression to match 'name' value
        name_match = re.search(r'name\s*=\s*"(.*?)"', content)
        name = name_match.group(1) if name_match else None
        
        # Regular expression to match the 'search' field content and extract 'index' and 'source'
        search_match = re.search(r'search\s*=\s*"(.*?)"', content, re.DOTALL)
        if search_match:
            search_content = search_match.group(1)
            index_match = re.search(r'index=(\S+)', search_content)
            source_match = re.search(r'source="([^"]+)"', search_content)
            index = index_match.group(1) if index_match else None
            source = source_match.group(1) if source_match else None
        else:
            index = None
            source = None

        return {
            'name': name,
            'index': index,
            'source': source
        }

def parse_all_terraform_files(directory):
    parsed_data = []
    for filename in os.listdir(directory):
        if filename.endswith(".tf"):  # Assuming Terraform files have a .tf extension
            file_path = os.path.join(directory, filename)
            data = parse_terraform_file(file_path)
            parsed_data.append({filename: data})
    
    return parsed_data

# Directory containing the Terraform files
directory_path = '/home/cam/detection-engineering/detections'
parsed_results = parse_all_terraform_files(directory_path)

# Print the parsed results
for result in parsed_results:
    print(result)
