#!/usr/bin/env python3
"""
Auto-commit README updater
Updates README.md file every minute and commits to GitHub
"""

import os
import subprocess
import time
from datetime import datetime

# Configuration
README_PATH = "README.md"  # Path to your README file
COMMIT_MESSAGE_PREFIX = "Auto-update README"
UPDATE_INTERVAL = 1  # seconds (1 minute)

def run_git_command(command):
    """Execute a git command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        return None

def update_readme():
    """Update the README file with current timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Read existing content
    if os.path.exists(README_PATH):
        with open(README_PATH, 'r') as f:
            content = f.read()
    else:
        content = "# Auto-Updated README\n\n"

    # Update or add the last updated line
    updated_marker = "Last updated:"
    lines = content.split('\n')

    # Check if "Last updated" line exists
    updated = False
    for i, line in enumerate(lines):
        if updated_marker in line:
            lines[i] = f"{updated_marker} {timestamp}"
            updated = True
            break

    if not updated:
        # Add the timestamp at the end
        lines.append(f"\n{updated_marker} {timestamp}")

    # Write back to file
    with open(README_PATH, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ README updated at {timestamp}")

def commit_and_push():
    """Commit changes and push to GitHub"""
    # Check if there are changes
    status = run_git_command("git status --porcelain")

    if not status:
        print("No changes to commit")
        return

    # Add the README file
    if run_git_command(f"git add {README_PATH}") is not None:
        print("✓ Changes staged")

    # Commit with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"{COMMIT_MESSAGE_PREFIX} - {timestamp}"

    if run_git_command(f'git commit -m "{commit_msg}"') is not None:
        print(f"✓ Changes committed: {commit_msg}")

    # Push to remote
    if run_git_command("git push") is not None:
        print("✓ Changes pushed to GitHub")
    else:
        print("✗ Failed to push changes")

def main():
    """Main loop"""
    print("Starting auto-commit README updater...")
    print(f"Update interval: {UPDATE_INTERVAL} seconds")
    print("Press Ctrl+C to stop\n")

    # Check if we're in a git repository
    if run_git_command("git rev-parse --git-dir") is None:
        print("Error: Not in a git repository!")
        print("Please run this script from within your git repository.")
        return

    try:
        while True:
            print(f"\n--- Update cycle at {datetime.now().strftime('%H:%M:%S')} ---")

            # Update README
            update_readme()

            # Commit and push
            commit_and_push()

            # Wait for next update
            print(f"Waiting {UPDATE_INTERVAL} seconds until next update...")
            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nStopping auto-commit script. Goodbye!")

if __name__ == "__main__":
    main()
