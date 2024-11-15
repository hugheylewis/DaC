import subprocess
import os
import sys
import time

# Define the repository path
repo_path = '/home/cam/detection-engineering/detections'

def run_git_command(command):
    from validation import colorize  # prevents circular import errors
    """Runs a git command and returns output, or exits if an error occurs."""
    try:
        result = subprocess.run(command, cwd=repo_path, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        if 'Your branch is up to date' in e.stdout:
            print("Your branch is up to date with 'origin/main'.\nNothing to commit, working tree clean. Exiting...")
            sys.exit(0)
        print(colorize("ERROR!", "\033[31m", True) + f" Could not run command '{' '.join(command)}': {e.stderr}")
        print(e.output)
        pull_from_github = None
        if 'git pull' in e.stderr:
            pull_from_github = input("\nWould you like to attempt a 'git pull' to integrate remote changes and try again? [Y/n] ")
            while pull_from_github not in ['Y', 'n']:
                if pull_from_github is not None:
                    print(f"{pull_from_github}: invalid answer. Please enter 'Y' or 'n'")
                pull_from_github = input("Would you like to attempt a 'git pull' to integrate remote changes and try again? [Y/n] ")
                if pull_from_github == 'Y':
                    print("Pulling from remote repository to integrate changes...")
                    time.sleep(0.25)
                    try:
                        run_git_command(["git", "pull", "origin", "main"])
                        print("Successfully pulled the latest changes from the repository.")
                    except subprocess.CalledProcessError as e:
                        print(f"Error occurred while performing git pull: {e}")
                    except Exception as e:
                        print(f"Unexpected error: {e}")
                else:
                    print("Remote changes will not be integrated. Exiting...")
                    time.sleep(0.25)
                    sys.exit(1)
        # else:
        #     print("Detections will not be pushed to GitHub. Exiting...")
        #     sys.exit(0)

def stage_commit_push():
    from validation import colorize # prevents circular import errors
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        print(colorize("ERROR!", "\033[31m", True) + f" {repo_path} is not a Git repository: a '.git' directory was not found")
        sys.exit(1)
    
    print("Staging changes...")
    run_git_command(["git", "add", "."])
    
    commit_message = input("Enter commit message: ")
    while not commit_message:
        print(colorize("ERROR!", "\033[31m", True) + " Commit message cannot be empty.")
        commit_message = input("Enter commit message: ")
    print("Committing changes...")
    time.sleep(0.25)
    run_git_command(["git", "commit", "-m", commit_message])
    
    # Push to remote
    print("Pushing to remote repository...")
    run_git_command(["git", "push", "-u", "origin", "main"])
    print("Changes pushed successfully.")

if __name__ == "__main__":
    stage_commit_push()
