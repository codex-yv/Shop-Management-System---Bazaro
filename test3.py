import git
import os
import time
from pathlib import Path

import git.repo

current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
local_path = current_dir / "server"
repo_url = "https://github.com/codex-yv/server.git"

commit_message = f"automated commit at {time.strftime('%Y-%m-%d %H:%M:%S')}"

# Check if the directory exists and is a valid git repo
if not os.path.exists(local_path):
    # print("Cloning repo...")
    repo = git.Repo.clone_from(repo_url, local_path)
elif os.path.isdir(local_path) and not os.path.exists(os.path.join(local_path, '.git')):
    # print(f"The directory {local_path} exists but is not a valid git repo, initializing repo")
    repo = git.Repo.init(local_path)
else:
    repo = git.Repo(local_path)

# Navigate to repo
os.chdir(local_path)

# Add untracked files
untracked_files = repo.untracked_files
if untracked_files:
    # print("Untracked files:", untracked_files)
    for file in untracked_files:
        try:
            repo.git.add(file)
        except Exception as e:
            print(f"Error adding {file} : {e}")

# Add modified files
modified_files = [item.a_path for item in repo.index.diff(None)]
if modified_files:
    # print("Modified files:", modified_files)
    for file in modified_files:
        try:
            repo.git.add(file)
        except Exception as e:
            print(f"Error adding {file} : {e}")

# Handle empty directories
for root, dirs, files in os.walk(local_path):
    for dir in dirs:
        dir_path = os.path.join(root, dir)
        if not os.listdir(dir_path):
            gitkeep_path = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write("# Placeholder to keep empty directories in git.")
                repo.git.add(gitkeep_path)
                # print(f"Added .gitkeep in path: {dir_path}")

status = repo.git.status()
# print("Status after adding files:", status)

# Commit and push changes
if repo.is_dirty():
    try:
        repo.index.commit(commit_message)
        origin = repo.remote(name='origin')
        origin.push()
        # print("Changes successfully committed and pushed to the repository.")
    except Exception as e:
        print(f"Error during committing and pushing changes: {e}")
else:
    print("No changes in the repository to commit.")
