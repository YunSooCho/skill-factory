#!/usr/bin/env python3
"""
Git Helper for Skill Factory

Automated Git operations:
- Auto-commmit when files change
- Automatic push to GitHub
- Branch management
- Tagging for releases

Usage:
    python3 git_helper.py commit --message "feat: Add service-name"
    python3 git_helper.py push
    python3 git_helper.py auto --check-interval 60
"""

import argparse
import subprocess
import time
from pathlib import Path
from typing import Optional


class GitHelper:
    """Helper for Git operations in Skill Factory"""

    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)

    def run_git(self, args: list) -> tuple[int, str, str]:
        """Run git command and return (exit_code, stdout, stderr)"""
        full_cmd = ["git"] + args
        result = subprocess.run(
            full_cmd,
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr

    def status(self) -> dict:
        """Get git status"""
        code, stdout, stderr = self.run_git(["status", "--porcelain"])
        return {
            "has_changes": bool(stdout.strip()),
            "output": stdout,
            "error": stderr
        }

    def add(self, files: list = None):
        """Stage files for commit"""
        if files is None:
            # Default files to add
            files = ["SERVICES_SPEC.md", "services/"]

        for f in files:
            self.run_git(["add", f])

    def commit(self, message: str, auto_add: bool = True) -> bool:
        """
        Commit changes

        Args:
            message: Commit message
            auto_add: Automatically stage all changes

        Returns:
            True if successful, False otherwise
        """
        if auto_add:
            self.add()

        code, stdout, stderr = self.run_git(["commit", "-m", message])

        if code == 0:
            print(f"✅ Commit successful: {message}")
            return True
        else:
            if stderr.strip() == "":
                # No changes to commit
                print(f"ℹ️  No changes to commit")
                return False
            else:
                print(f"❌ Commit failed: {stderr}")
                return False

    def push(self, remote: str = "origin", branch: str = None) -> bool:
        """
        Push changes to remote

        Args:
            remote: Remote repository name (default: origin)
            branch: Branch name (default: current branch)

        Returns:
            True if successful, False otherwise
        """
        if branch is None:
            code, stdout, _ = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])
            branch = stdout.strip()

        args = ["push", remote, branch]
        code, stdout, stderr = self.run_git(args)

        if code == 0:
            print(f"✅ Push successful: {remote}/{branch}")
            return True
        else:
            print(f"❌ Push failed: {stderr}")
            return False

    def auto_commit(self, message: str, push: bool = False) -> bool:
        """
        Auto-commit and optionally push

        Args:
            message: Commit message
            push: Whether to push after commit

        Returns:
            True if successful, False otherwise
        """
        status = self.status()

        if not status["has_changes"]:
            print("ℹ️  No changes to commit")
            return False

        committed = self.commit(message, auto_add=True)

        if committed and push:
            self.push()

        return committed

    def watch_and_commit(self, check_interval: int = 60):
        """
        Watch for changes and auto-commit

        Args:
            check_interval: Check interval in seconds
        """
        print(f"👀 Watching for changes every {check_interval} seconds...")

        try:
            while True:
                status = self.status()

                if status["has_changes"]:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    message = f"Auto-commit: {timestamp}"
                    self.auto_commit(message, push=True)

                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n👋 Stopping watch")

    def get_current_branch(self) -> Optional[str]:
        """Get current branch name"""
        code, stdout, _ = self.run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if code == 0:
            return stdout.strip()
        return None

    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get remote repository URL"""
        code, stdout, _ = self.run_git(["remote", "get-url", remote])
        if code == 0:
            return stdout.strip()
        return None


def main():
    parser = argparse.ArgumentParser(description="Git helper for Skill Factory")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Commit command
    commit_parser = subparsers.add_parser("commit", help="Commit changes")
    commit_parser.add_argument("--message", "-m", required=True, help="Commit message")
    commit_parser.add_argument("--push", action="store_true", help="Push after commit")

    # Push command
    push_parser = subparsers.add_parser("push", help="Push changes")

    # Status command
    subparsers.add_parser("status", help="Show status")

    # Auto command
    auto_parser = subparsers.add_parser("auto", help="Auto-commit and push")
    auto_parser.add_argument("--check-interval", type=int, default=60, help="Check interval (seconds)")

    args = parser.parse_args()

    git = GitHelper()

    if args.command == "commit":
        git.commit(args.message, auto_add=True)
        if args.push:
            git.push()

    elif args.command == "push":
        git.push()

    elif args.command == "status":
        status = git.status()
        if status["has_changes"]:
            print("Changes detected:")
            print(status["output"])
        else:
            print("No changes")

    elif args.command == "auto":
        git.watch_and_commit(check_interval=args.check_interval)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()