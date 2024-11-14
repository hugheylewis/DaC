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

def check_fields(data):
    print("Verifying all required fields are present...")
    time.sleep(0.25)
    for field in required_fields:
        if 'module' in data:
            modules = data['module']
            
            if isinstance(modules, list): # If 'module' is a list
                for module_data in modules:
                    for k, v in module_data.items():
                        if field not in k:
                            print(colorize("ERROR!", "\033[31m", True) + f" Missing field: '{field}'")
                            try:
                                issues.append(f"'{field}' is missing from your {file.name} file in a module")
                            except AttributeError as e:
                                issues.append(f"'{field}' is missing from one of your files")
                            return False

            elif isinstance(modules, dict): # If 'module' is a dictionary
                for module_name, module_data in modules.items():
                  if field not in module_data:
                        print(colorize("ERROR!", "\033[31m", True) + f" Missing field: '{field}' in module '{module_name}'")
                        issues.append(f"'{field}' is missing from your {file.name} file in module '{module_name}'")
                        return False
    print(colorize("Success!", "\033[32m", True) + " All required fields are present.")
    return True

if __name__ == "__main__":
    issues = []
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
        issues.append(f"'terraform fmt' returned code {fmt_return_code}")
    time.sleep(0.25)

    for root, dirs, files in os.walk('/home/cam/detection-engineering/detections'):
        for file in files:
            if file.endswith(".tf"):
                full_path = os.path.join(root, file)
                with open(full_path, 'r') as file:
                    alert = hcl2.load(file)
                    json_converted = json.dumps(alert, indent=2)
                    json_data = json.loads(json_converted)
                    

    if len(issues) == 0 and check_fields(json_data):
        push_to_github = input("\n\nAll tests pass! Do you want to push these detections to GitHub? [Y/n] ")
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
        print(f"\n\n{len(issues)} issues were found in your Terraform files:")
        for i in issues:
            print(f"\t- {i}")
                    
