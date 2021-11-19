import os
import re
from typing import Iterable

import keepachangelog
import requests


def is_dry_run() -> bool:
    return os.getenv("PLUGIN_DRY_RUN", os.getenv("DRONE_PULL_REQUEST"))


class GitHub:
    def __init__(self):
        token = os.getenv('PLUGIN_GITHUB_TOKEN', os.getenv("DRONE_GIT_PASSWORD"))
        if not token:
            raise Exception("github_token parameter must be provided as DRONE_GIT_PASSWORD environment variable is not set.")

        github_link = os.getenv("DRONE_REPO_LINK")[:-len(os.getenv("DRONE_REPO"))]
        self.base_url = f"{github_link}api/v3/repos/{os.getenv('DRONE_REPO')}"
        self.client = requests.Session()
        self.client.headers = {'Authorization': f"token {token}", "Accept": "application/vnd.github.v3+json"}

    def get(self, uri: str, raise_for_status: bool = True) -> requests.Response:
        response = self.client.get(
            url=f"{self.base_url}{uri}",
        )
        if raise_for_status:
            response.raise_for_status()
        return response

    def post(self, uri: str, content: dict) -> requests.Response:
        response = self.client.post(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to POST to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

    def put(self, uri: str, content: dict) -> requests.Response:
        response = self.client.put(
            url=f"{self.base_url}{uri}",
            json=content
        )
        if not response:
            raise Exception(f"Unable to PUT to {response.url}: {response.text} (HTTP {response.status_code})")
        response.raise_for_status()
        return response

    def get_last_commit(self, branch: str) -> str:
        return self.get(f"/branches/{branch}").json()['commit']['sha']

    def commit(self, file_path: str) -> str:
        with open(file_path) as file:
            content = file.read()
        return self.post(
            "/git/blobs",
            {
                "content": content,
                "encoding": "utf-8"
            }
        ).json()['sha']

    def push_files(self, last_commit_sha: str, *file_paths: str) -> str:
        return self.post(
            "/git/trees",
            {
                "base_tree": last_commit_sha,
                "tree": [
                    {
                        "path": file_path,
                        "mode": "100644",
                        "type": "blob",
                        "sha": self.commit(file_path)
                    }
                    for file_path in file_paths
                ]
            }
        ).json()['sha']

    def update_last_commit(self, branch: str, new_commit: str):
        self.post(
            f"/git/refs/heads/{branch}",
            {
                "ref": f"refs/heads/{branch}",
                "sha": new_commit
            }
        )

    def commit_and_push(self, user_name: str, user_email: str, branch: str, message: str, file_paths: Iterable[str]):
        previous_protection = self.disable_protection(branch)
        try:
            last_commit_sha = self.get_last_commit(branch)
            if not is_dry_run():
                tree_sha = self.push_files(last_commit_sha, *file_paths)
                new_commit = self.post(
                    "/git/commits",
                    {
                        "message": message,
                        "author": {
                            "name": user_name,
                            "email": user_email
                        },
                        "parents": [
                            last_commit_sha
                        ],
                        "tree": tree_sha
                    }
                ).json()['sha']
                self.update_last_commit(branch, new_commit)
        finally:
            if previous_protection and not is_dry_run():
                self.set_protection(branch, previous_protection)

    def get_protection(self, branch: str) -> dict:
        response = self.get(
            f"/branches/{branch}/protection", raise_for_status=False
        )

        if 404 == response.status_code:
            reason = response.json()["message"]
            if "Branch not protected" == reason:
                return {}
            raise Exception(f"The provided token does not allow to fetch {branch} branch protection. Related user must be Admin of this repository.")

        response.raise_for_status()
        return response.json()

    def set_protection(self, branch: str, protection: dict) -> dict:
        required_pull_request_reviews = {
            "dismissal_restrictions": {
                "users": [user["login"] for user in dismissal_restrictions.get("users", [])],
                "teams": [team["slug"] for team in dismissal_restrictions.get("teams", [])],
            } if (dismissal_restrictions := required_pull_request_reviews.get("dismissal_restrictions")) else {},
            "dismiss_stale_reviews": required_pull_request_reviews.get("dismiss_stale_reviews"),
            "require_code_owner_reviews": required_pull_request_reviews.get("require_code_owner_reviews"),
        } if (required_pull_request_reviews := protection.get("required_pull_request_reviews")) else None
        restrictions = {
            "users": [user["login"] for user in restrictions.get("users", [])],
            "teams": [team["slug"] for team in restrictions.get("teams", [])],
            "apps": restrictions.get("apps"),
        } if (restrictions := protection.get("restrictions")) else None
        return self.put(
            f"/branches/{branch}/protection",
            content={
                "required_status_checks": protection.get("required_status_checks"),
                "enforce_admins": (protection.get("enforce_admins") or {}).get("enabled"),
                "required_pull_request_reviews": required_pull_request_reviews,
                "restrictions": restrictions,
                "required_linear_history": (protection.get("required_linear_history") or {}).get("enabled"),
                "allow_force_pushes": (protection.get("allow_force_pushes") or {}).get("enabled"),
                "allow_deletions": (protection.get("allow_deletions") or {}).get("enabled"),
            }
        ).json()

    def disable_protection(self, branch: str) -> dict:
        previous_protection = self.get_protection("master")
        if previous_protection and not is_dry_run():
            self.set_protection(branch, {
                "required_status_checks": None,
                "enforce_admins": previous_protection.get("enforce_admins"),
                "required_pull_request_reviews": None,
                "restrictions": previous_protection.get("restrictions"),
                "required_linear_history": previous_protection.get("required_linear_history"),
                "allow_force_pushes": previous_protection.get("allow_force_pushes"),
                "allow_deletions": previous_protection.get("allow_deletions"),
            })
        return previous_protection


def update_version_in_file(version_file_path: str, new_version: str):
    with open(version_file_path) as version_file:
        previous_content = version_file.read()

    new_content = re.sub('__version__ = ".*"', f'__version__ = "{new_version}"', previous_content)

    if not is_dry_run():
        with open(version_file_path, "wt") as version_file:
            version_file.write(new_content)


def bump_version():
    if os.getenv('PLUGIN_SKIP_COMMIT_AUTHOR') == os.getenv("DRONE_COMMIT_AUTHOR"):
        print(f"Skipping version bump as commit author ({os.getenv('DRONE_COMMIT_AUTHOR')}) is {os.getenv('PLUGIN_SKIP_COMMIT_AUTHOR')}.")
        return

    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    # Compute the new version number and update CHANGELOG
    new_version = keepachangelog.release(changelog_path)
    if not new_version:
        if os.getenv("PLUGIN_MANDATORY_CHANGELOG_ENTRY"):
            raise Exception(f"{changelog_path} must contains a description of the changes (within Unreleased section).")

        print("Skipping version bump as there is nothing to release.")
        return

    print(f"Bumping version to {new_version}.")

    files_to_commit = [changelog_path]

    # Update version in source code
    version_file_path = os.getenv('PLUGIN_VERSION_FILE_PATH')
    if version_file_path:
        update_version_in_file(version_file_path, new_version)
        files_to_commit.append(version_file_path)

    github = GitHub()

    github.commit_and_push(
        user_name=os.getenv('PLUGIN_USER_NAME', os.getenv("DRONE_COMMIT_AUTHOR_NAME")),
        user_email=os.getenv('PLUGIN_USER_EMAIL', os.getenv("DRONE_COMMIT_AUTHOR_EMAIL")),
        branch=os.getenv("DRONE_TARGET_BRANCH"),
        message=f"Release {new_version}",
        file_paths=files_to_commit
    )


if __name__ == "__main__":
    bump_version()
