# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.5] - 2023-09-20
### Fixed
- Do not send the deprecated `required_status_checks`.`contexts` anymore.

## [1.2.4] - 2023-08-08
### Fixed
- Make sure to sync the `required_approving_review_count` setting when protection is being reactivated

## [1.2.3] - 2023-06-07
### Fixed
- Only release for amd64 platform (avoid unknown platform image).

## [1.2.1] - 2023-06-07
### Fixed
- Use latest GH actions.
- Update dependencies to latest version.

## [1.2.0] - 2023-05-24
### Added
- Add link to ticket in changelog, based on the key in the branch name.

## [1.1.6] - 2022-09-08
### Fixed
- Protection is now properly re-activated even if both contexts and checks required_status_checks are empty.

## [1.1.5] - 2022-09-07
### Fixed
- Protection is now properly re-activated even if required_status_checks are already there.

## [1.1.4] - 2021-11-19
### Fixed
- Avoid failure if there is no dismissal_restrictions set.

## [1.1.3] - 2021-11-18
### Fixed
- Avoid failure if there is no dismissal_restrictions set.

## [1.1.2] - 2021-11-18
### Fixed
- Avoid failure if there is no restrictions set.

## [1.1.1] - 2021-10-19
### Fixed
- Add an explicit error message in case user is not admin of the repository.

## [1.1.0] - 2021-10-05
### Added
- Added a dry-run mode activated by default for pull-requests.
- Allow to require a changelog entry.

## [1.0.4] - 2021-09-30
### Fixed
- Version bump is now properly performed even if there is a branch protection on specific users.

## [1.0.3] - 2021-09-29
### Fixed
- Protection is now properly re-activated even if pull request reviews and/or status checks are not required.

## [1.0.2] - 2021-09-16
### Fixed
- Version bump is now properly performed even if there is no branch protection.

## [1.0.1] - 2021-08-05
### Fixed
- Version bump is now properly performed even if previous versions do not have the same number of digits.

### Added
- Log the new version that will be used.

## [1.0.0] - 2021-05-27
### Changed
- Do not fail but instead skip version bump if there is nothing to release.

## [0.2.1] - 2021-05-19
### Fixed
- Add missing `requests` dependency.

## [0.2.0] - 2021-05-18
### Added
- Add `github_token` parameter.
- Add `user_name` parameter.
- Add `user_email` parameter.

## [0.1.0] - 2021-05-17
### Added
- Add `skip_commit_author` parameter.

## [0.0.3] - 2021-04-22
### Fixed
- Handle the fact that `WORKDIR` changes when using as a drone plugin.

## [0.0.2] - 2021-04-22
### Fixed
- Include python script in Docker image.

## [0.0.1] - 2021-04-21
### Added
- Initial release.

[Unreleased]: https://github.com/ets-infra/drone-bump-version/compare/1.2.5...master
[1.2.5]: https://github.com/ets-infra/drone-bump-version/compare/1.2.4...1.2.5
[1.2.4]: https://github.com/ets-infra/drone-bump-version/compare/1.2.3...1.2.4
[1.2.3]: https://github.com/ets-infra/drone-bump-version/compare/1.2.2...1.2.3
[1.2.2]: https://github.com/ets-infra/drone-bump-version/compare/1.2.1...1.2.2
[1.2.1]: https://github.com/ets-infra/drone-bump-version/compare/1.2.0...1.2.1
[1.2.0]: https://github.com/ets-infra/drone-bump-version/compare/1.1.6...1.2.0
[1.1.6]: https://github.com/ets-infra/drone-bump-version/compare/1.1.5...1.1.6
[1.1.5]: https://github.com/ets-infra/drone-bump-version/compare/1.1.4...1.1.5
[1.1.4]: https://github.com/ets-infra/drone-bump-version/compare/1.1.3...1.1.4
[1.1.3]: https://github.com/ets-infra/drone-bump-version/compare/1.1.2...1.1.3
[1.1.2]: https://github.com/ets-infra/drone-bump-version/compare/1.1.1...1.1.2
[1.1.1]: https://github.com/ets-infra/drone-bump-version/compare/1.1.0...1.1.1
[1.1.0]: https://github.com/ets-infra/drone-bump-version/compare/1.0.4...1.1.0
[1.0.4]: https://github.com/ets-infra/drone-bump-version/compare/1.0.3...1.0.4
[1.0.3]: https://github.com/ets-infra/drone-bump-version/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/ets-infra/drone-bump-version/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/ets-infra/drone-bump-version/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/ets-infra/drone-bump-version/compare/0.2.1...1.0.0
[0.2.1]: https://github.com/ets-infra/drone-bump-version/compare/0.2.0...0.2.1
[0.2.0]: https://github.com/ets-infra/drone-bump-version/compare/0.1.0...0.2.0
[0.1.0]: https://github.com/ets-infra/drone-bump-version/compare/0.0.3...0.1.0
[0.0.3]: https://github.com/ets-infra/drone-bump-version/compare/0.0.2...0.0.3
[0.0.2]: https://github.com/ets-infra/drone-bump-version/compare/0.0.1...0.0.2
[0.0.1]: https://github.com/ets-infra/drone-bump-version/releases/tag/0.0.1
