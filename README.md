# Supported tags and respective Dockerfile links

- [`1.0.0`, `latest`](https://github.com/ets-infra/drone-bump-version/blob/master/1/Dockerfile)

# Quick reference (cont.)

- **Where to file issues**: [https://github.com/ets-infra/drone-bump-version/issues](https://github.com/ets-infra/drone-bump-version/issues)

# What is the purpose of this image?

[Drone](https://www.drone.io) plugin to bump version based on changelog following [keepachangelog](https://keepachangelog.com/en/1.1.0/) format.

<p align="center">
    <a href="https://www.drone.io"><img alt="drone logo" src="https://raw.githubusercontent.com/drone/brand/master/logos/png/dark/drone-logo-png-dark-128.png"></a>
</p>

The following steps are executed by this plugin:

1. Guess new version number based on the `Unreleased` changelog section. If no changes can be found, the following steps are not performed.
2. Move `Unreleased` changelog section within a new section for this new version.
3. Optional: Update `__version__` value in version file.
4. Commit and push changelog (and version file if provided).

| Parameter | Description |
|:---|---|
| changelog_path | Path to the changelog. Default to `CHANGELOG.md` in current folder. |
| version_file_path | Path to the python file containing the version. If not provided, no file will be updated. |
| skip_commit_author | If provided and the value matches the one from [the commit author user name](https://docs.drone.io/pipeline/environment/reference/drone-commit-author/), this plugin will not do anything. |
| github_token | Token (repo permission) used to commit and update repository permissions temporarily. Default to [the drone GIT password](https://docs.drone.io/server/reference/drone-git-password/) (if available). Related user needs to have admin role in repository. |
| user_name | Name of the GIT commit user. Default to [the drone GIT user name](https://docs.drone.io/pipeline/environment/reference/drone-commit-author-name/). |
| user_email | email of the GIT commit user. Default to [the drone GIT user email](https://docs.drone.io/pipeline/environment/reference/drone-commit-author-email/). |

# How to use this image

## Add a step to your drone pipeline

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: bump_version
  image: etsinfra/drone-bump-version:latest
  settings:
    changelog_path: custom_folder/CHANGELOG.md
    version_file_path: custom_folder/__init__.py
    github_token: cc1cc11111111ccc1c11c1cc1ccc1c1cc1111c1c
    user_name: user
    user_email: user@email.com
```
