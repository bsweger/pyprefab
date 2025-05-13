# pyprefab

A template-driven command line interface (CLI) that creates the scaffolding
for a fully-functional, modern Python package. The goal of pyprefab is to get
you straight to writing application code by handling project startup tasks
like logging setup and creating a test harness.

![pyprefab demo](https://raw.githubusercontent.com/bsweger/pyprefab/main/docs/source/_static/pyprefab-demo.gif)

The scaffolding includes:

- package files in the [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) format
- `pyproject.toml` with [dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/#dependency-groups)
- `CHANGELOG.md`, `CONTRIBUTING.md`, `.gitignore`, and `README.md`
- automated package versioning with [setuptools-scm](https://pypi.org/project/setuptools-scm/)
- [structlog](https://www.structlog.org/)-based pre-configured logging
- a [pytest](https://docs.pytest.org)-based test harness
- a [pre-commit](https://pre-commit.com/) configuration with common plugins like
[ruff](https://docs.astral.sh/ruff/) for linting (optional)
- GitHub workflow that automatically runs code checks, tests, and a test
coverage report
- GitHub workflow for publishing the package to PyPI

## Quickstart

If you have `uv` installed,
[`uv tool run`](https://docs.astral.sh/uv/reference/cli/#uv-tool-run) is the
fastest way to create a new Python package with pyprefab:

```sh
uvx pyprefab
```

Otherwise, use `pip` or `pipx` to install pyprefab:

```sh
python -m pip install pyprefab

python -m pyprefab
```

## Project setup

See [CONTRIBUTING.MD](CONTRIBUTING.md) for information on setting up
a local development environment for pyprefab.
