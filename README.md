# Supported tags and respective Dockerfile links

- [`0.0.1`, `latest`](https://github.com/ets-infra/drone-bump-version/blob/master/0/Dockerfile)

# Quick reference (cont.)

- **Where to file issues**: [https://github.com/ets-infra/drone-bump-version/issues](https://github.com/ets-infra/drone-bump-version/issues)

# What is the purpose of this image?

[Drone](https://www.drone.io) plugin to bump version based on changelog following [keepachangelog](https://keepachangelog.com/en/1.1.0/) format.

<p align="center">
    <a href="https://www.drone.io"><img alt="drone logo" src="https://raw.githubusercontent.com/drone/brand/master/logos/png/dark/drone-logo-png-dark-128.png"></a>
</p>

The following steps are executed by this plugin:

1. Guess new version number based on the `Unreleased` changelog section.
2. Move `Unreleased` changelog section within a new section for this new version.
3. Optional: Update `__version__` value in version file.

| Parameter | Description |
|:---|---|
| changelog_path | Path to the changelog. Default to `CHANGELOG.md` in current folder. |
| version_file_path | Path to the python file containing the version. If not provided, no file will be updated. |

# How to use this image

## Add a step to your drone pipeline

```yaml
kind: pipeline
type: docker
name: default

steps:
- name: tag
  image: etsinfra/drone-bump-version:0.0.1
  settings:
    changelog_path: custom_folder/CHANGELOG.md
    version_file_path: custom_folder/__init__.py
```
