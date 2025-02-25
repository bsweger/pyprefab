# Changelog

All notable changes to `pyprefab` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com), and the
project uses [Semantic Versioning](https://semver.org/).

## 0.5.3

### Changed

- Entry point of generated app now displays additional output
- `--docs` parameter can now be set interactively
- README examples reflect that `--name` and `--docs` options are interactive

## 0.5.2

### Changed

- Improve CHANGELOG aesthetics
- Fail when target directory is not empty (instead of prompting)
- Add colors and default values to CLI prompts

### Fixed

- Ensure pyprefab can run as `python -m pyprefab`

## 0.5.1

### Fixed

- Fail docs build GitHub action on Sphinx error or warning
- Correct pyprefab version retrieved during doc build

## 0.5.0

### Added

- Sphinx-based project documentation (published on GitHub pages)
- New CLI `--docs` option to include skeleton documentation in created package

### Fixed

- Add escape character to quotation marks in author name and project description

## 0.4.0

### Added

- New templates for GitHub workflows: ci (linting, tests, and coverage),
  publishing to TestPyPI, and publishing to PyPI
- Project changelog
- New CHANGELOG.md template
- New CONTRIBUTING.md template

### Changed

- Add CLI prompts as an alternate to passing command options
- `--directory` option renamed to `--dir`
- Prompt user when specified project directory is not empty
- List created package components on README.md

### Fixed

- Correct CLI example on README.md

## 0.3.2

### Changed

- Rename CLI command to `pyprefab`

## 0.3.1

### Added

- New templates for generating Python package boilerplate: .gitignore,
  README.md, app.py

### Changed

- Rename project to `pyprefab`

### Removed

- Removed sample `hello_world` module in favor of template-driven boilerplate

## 0.3.0

### Added

- Added `pyproject.toml` template as the first piece of template-driven Python
  boilerplate

### Removed

- Removed artifacts from prior iteration of `pyprefab` that pre-dates the
  template-driven approach
