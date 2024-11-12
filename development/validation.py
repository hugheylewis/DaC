from python_terraform import *
from termcolor import colored
import hcl2
import sys
import os
import json
import time

def colorize(text, color_code, bold=False):
    bold_code = "\033[1m" if bold else ""
    reset_code = "\033[0m"
    return f"{bold_code}{color_code}{text}{reset_code}"

def check_fields(data):
    print("Verifying all required fields are present...")
    time.sleep(0.25)
    for field in required_fields:
        if 'module' in data:
            for module in data['module']:  # Assuming there could be multiple modules in the list, check each one
                if 'user_added_to_admin_group' in module:
                    user_group = module['user_added_to_admin_group']
                    if field not in user_group:
                        print(colorize("ERROR!", "\033[31m", True) + f" Missing field: '{field}'")
                        issues.append(f"'{field}' is missing from your {file.name} file")
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

    for root, dirs, files in os.walk('/home/user/detection-engineering/detections'):
        for file in files:
            if file.endswith(".tf"):
                full_path = os.path.join(root, file)
                with open(full_path, 'r') as file:
                    alert = hcl2.load(file)
                    json_converted = json.dumps(alert, indent=2)
                    json_data = json.loads(json_converted)
                    

    if len(issues) == 0 and check_fields(json_data):
        print("\n\nAll tests pass! You can now push these detections to GitHub.")
    else:
        print(f"\n\n{len(issues)} issues were found in your Terraform files:")
        for i in issues:
            print(f"\t- {i}")
                    
