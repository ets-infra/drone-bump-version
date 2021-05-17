import os
import re

import keepachangelog


def update_version_in_file(new_version: str):
    version_file_path = os.getenv('PLUGIN_VERSION_FILE_PATH')
    if not version_file_path:
        return

    with open(version_file_path) as version_file:
        previous_content = version_file.read()

    new_content = re.sub('__version__ = ".*"', f'__version__ = "{new_version}"', previous_content)

    with open(version_file_path, "wt") as version_file:
        version_file.write(new_content)


def bump_version():
    if os.getenv('PLUGIN_SKIP_COMMIT_AUTHOR') == os.getenv("DRONE_COMMIT_AUTHOR"):
        return

    changelog_path = os.getenv('PLUGIN_CHANGELOG_PATH', "CHANGELOG.md")
    # Compute the new version number and update CHANGELOG
    new_version = keepachangelog.release(changelog_path)
    # Update version in source code
    update_version_in_file(new_version)


if __name__ == "__main__":
    bump_version()
