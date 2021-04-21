# Bump version based on changelog

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
