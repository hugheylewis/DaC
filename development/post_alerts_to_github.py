from termcolor import colored
from validation import colorize
import subprocess
import os
import sys

# Define the repository path
repo_path = '/home/cam/detection-engineering/detections'

def run_git_command(command):
    """Runs a git command and returns output, or exits if an error occurs."""
    try:
        result = subprocess.run(command, cwd=repo_path, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(colorize("ERROR!", "\033[31m", True) + f" Could not run command {' '.join(command)}: {e.stderr}")
        sys.exit(1)

def main():
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(colorize("ERROR!", "\033[31m", True) + f" {repo_path} is not a Git repository: a '.git' directory was not found")
        sys.exit(1)
    
    # status_output = run_git_command(["git", "status", "--porcelain"])
    # if not status_output.strip():
    #     print("No changes to commit.")
    #     sys.exit(0)
    
    print("Staging changes...")
    run_git_command(["git", "add", "."])
    
    commit_message = input("Enter commit message: ")
    while not commit_message:
        print(colorize("ERROR!", "\033[31m", True) + " Commit message cannot be empty.")
        commit_message = input("Enter commit message: ")
    print("Committing changes...")
    run_git_command(["git", "commit", "-m", commit_message])
    
    # Push to remote
    print("Pushing to remote repository...")
    run_git_command(["git", "push", "-u", "origin", "main"])
    print("Changes pushed successfully.")

if __name__ == "__main__":
    main()
