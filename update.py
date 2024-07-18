import os
import subprocess

def update_app():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(repo_dir)
    
    # Fetch the latest changes from the repo
    subprocess.run(['git', 'fetch'])
    
    # Check if there are updates
    local_commit = subprocess.check_output(['git', 'rev-parse', '@']).strip()
    remote_commit = subprocess.check_output(['git', 'rev-parse', '@{u}']).strip()
    
    if local_commit != remote_commit:
        print("Updating application...")
        subprocess.run(['git', 'pull'])
        subprocess.run(['pyinstaller', '--onefile', 'main.py'])
        print("Update completed. Restart the application.")
    else:
        print("Application is up to date.")

if __name__ == "__main__":
    update_app()
