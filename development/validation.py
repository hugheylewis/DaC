from python_terraform import *
from termcolor import colored
import hcl2
import sys
import os
import json
import time
import github

def colorize(text, color_code, bold=False):
    bold_code = "\033[1m" if bold else ""
    reset_code = "\033[0m"
    return f"{bold_code}{color_code}{text}{reset_code}"

def check_fields(data, file_name, missing_fields):
    # Track the missing fields for the current file
    file_missing_fields = []  

    for field in required_fields:
        if 'module' in data:
            modules = data['module']

            if isinstance(modules, list):  # If 'module' is a list
                for module_data in modules:
                    # Each module is a dictionary, where the module name is the key
                    for module_name, module_config in module_data.items():
                        # Check if the required field exists in the module's config
                        if field not in module_config:
                            file_missing_fields.append(f"'{field}' is missing in module '{module_name}' in file '{file_name}'")

            elif isinstance(modules, dict):  # If 'module' is a dictionary
                for module_name, module_data in modules.items():
                    # Check if the required field exists in the module's data
                    if field not in module_data:
                        file_missing_fields.append(f"'{field}' is missing in module '{module_name}' in file '{file_name}'")

    # After checking all fields, if there are missing fields, append them globally
    if file_missing_fields:
        missing_fields.extend(file_missing_fields)
        return False  # Return False if any fields are missing
    
    return True  # Return True if no fields are missing

if __name__ == "__main__":
    missing_fields = [] 
    required_fields = ['name', 'search', 'cron_schedule', 'is_scheduled', 'alert']
    terraform = Terraform(working_dir='/home/cam/detection-engineering/')
    validate_return_code, validate_stdout, validate_stderr = terraform.validate()
    fmt_return_code, fmt_stdout, fmt_stderr = terraform.fmt(diff=True)

    print("Running 'terraform validate'...")
    time.sleep(0.25)
    print(validate_stdout)
    time.sleep(0.25)

    print("Running 'terraform fmt'...")
    time.sleep(0.25)
    if fmt_return_code == 0 or fmt_return_code == 1:
        print(colorize("Success!", "\033[92m", True) + f" 'terraform fmt' returned code {fmt_return_code}.\n")
    else:
        print(colorize("ERROR!", "\033[31m", True) + f" 'terraform fmt' returned code {fmt_return_code}\n")
        missing_fields.append(f"'terraform fmt' returned code {fmt_return_code}")
    time.sleep(0.25)

    # Initialize a counter for the Terraform files
    tf_file_count = 0

    # Count the number of Terraform files to validate
    for root, dirs, files in os.walk('/home/cam/detection-engineering/detections'):
        for file_name in files:
            if file_name.endswith(".tf"):
                tf_file_count += 1

    print(f"\nEnsuring required fields are present in {tf_file_count} Terraform file(s)...\n")
    time.sleep(0.5)

    # Now validate each file
    for root, dirs, files in os.walk('/home/cam/detection-engineering/detections'):
        for file_name in files:
            if file_name.endswith(".tf"):
                full_path = os.path.join(root, file_name)
                with open(full_path, 'r') as tf_file:
                    alert = hcl2.load(tf_file)
                    json_converted = json.dumps(alert, indent=2)
                    json_data = json.loads(json_converted)

                    # Call check_fields with the correct file_name
                    if not check_fields(json_data, file_name, missing_fields):
                        print(colorize("ERROR!", "\033[31m", True) + f" Issues found in {file_name}")

    # After checking all files, check if there are any missing fields
    if len(missing_fields) == 0:
        push_to_github = input("\n" + colorize("Success!", "\033[92m", True) + " All tests pass! Do you want to push these detections to GitHub? [Y/n] ")
        while push_to_github not in ['Y', 'n']:
            print(f"{push_to_github}: invalid answer. Please enter 'Y' or 'n'")
            push_to_github = input("Do you want to push these detections to GitHub? [Y/n] ")
        if push_to_github == 'Y':
            print("Pushing to remote repository...")
            time.sleep(0.25)
            github.stage_commit_push()
        else:
            print("Detections will not be pushed to GitHub. Exiting...")
            sys.exit(0)
    else:
        print(f"{len(missing_fields)} issues were found in your Terraform files:")
        for i in missing_fields:
            print(f"\t- {i}")
