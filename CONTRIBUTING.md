# Contributing

This is a personal, very-part-time project, largely driven by my own opinions
about how best to configure a Python code base.

Contributions as described below are welcome.

## Reporting bugs

If something isn't working as described, or if you find a mistake in the
documentation, please feel free to report a bug by
[opening an issue](https://github.com/bsweger/pyprefab/issues).

## Contributing to the code base

Contributions to the code base are welcome. If you want to add a new feature,
please open an issue first. Because `pyprefab` is an opinion-drive personal
project, it's best to make sure our opinions are aligned before doing any work!

If you'd like to tackle an existing issue, please leave a comment on it.

### Creating your local development environment

For contributing to this code base, you'll need:

- A [GitHub account](https://github.com/)
- [Git](https://git-scm.com/) installed on your machine
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

> [!IMPORTANT]
> If you have an active Python virtual environment (for example, conda's
> base environment), you'll need to deactivate it before following the
> instructions below.

#### Configure git

1. On GitHub, [fork](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) this repository.

2. Clone the forked repository to your machine:

    ```bash
    git clone https://github.com/<username>/pyprefab.git
    cd pyprefab
    ```

3. **optional:** Set the `upstream` remote to sync your fork with the `pyprefab`
repository:

    ```bash
    git remote add upstream https://github.com/bsweger/pyprefab.git
    git fetch upstream
    ```

#### Install project and dependencies

1. From the root of the repo, create a virtual environment and install the
project dependencies. The
[`uv sync` command](https://docs.astral.sh/uv/reference/cli/#uv-sync) handles
installing Python, creating a virtual environment, and installing project
dependencies.

    ```bash
    uv sync
    ```

   (More information about how uv
    [finds or downloads a Python interpreter](https://docs.astral.sh/uv/reference/cli/#uv-python))

2. Run the [nox](https://nox.thea.codes/en/stable/)-based checks to ensure that
   everything works correctly:

    > [!TIP]
    > Prefixing python commands with `uv run` instructs uv to run the command
    > in the project's virtual environment, even if you haven't explicitly
    > activated it.

    ```bash
    uv run nox --tags checks
    ```

    The above command will run the checks against every version of Python
    supported by pyprefab. Alternately, you could save time by running the
    checks against a specific version of Python:

    ```bash
    uv run nox --tags checks --python 3.13
    ```

    GitHub actions will run the checks against all Python versions when
    you open a pull request.

### Make your changes

Once your development environment is set up, you can start making your changes.
Note that you can test your work in progress by running individual nox sessions
as you go:

- `nox -s lint` - Run the linter (ruff)
- `nox -s typecheck` - Run static type checking (mypy)
- `nox -s tests` - Run the test suite (will run on all supported Python versions)
- `nox -s docs` - Build the documentation
- `nox -s docs_serve` - Serve the documentation locally with auto-reload

To run a specific session with a specific Python version:

```bash
nox -s test-3.11
```

### Updating your development environment

If time has passed between your initial project setup and when you make changes
to the code, make sure your fork and development environment are up-to-date.

1. Sync your fork to the upstream repository:

    ```bash
    git checkout main
    git fetch upstream
    git rebase upstream/main
    git push origin main
    ```

2. Update your project dependencies:

    ```bash
    uv sync
    ```

### Adding project dependencies

If your change requires a new dependency, add it as follows:

```bash
uv add <dependency>
```

The [`uv add`](https://docs.astral.sh/uv/reference/cli/#uv-add) command will:

- Add the dependency to `pyproject.toml`
- Install the dependency into the project's virtual environment
- Update the project's lockfile (`uv.lock`)

Make sure to commit the updated versions of `pyproject.toml` and `uv.lock`.

### Updating snapshot tests

This project uses [`syrupy`](https://github.com/syrupy-project/syrupy) to run snapshot tests against the output of pyprefab's templates.

If you've added a new pyprefab template, add a test snapshot test for it in `test_templates.py`. Then, instruct syrupy to generate a snapshot for the new template:

```bash
uv run pytest --snapshot-update
```

### Updating documentation

This project uses [Sphinx](https://www.sphinx-doc.org/en/master/) and
[MyST-flavored markdown](https://myst-parser.readthedocs.io/en/latest/index.html)
for documentation.

Documentation updates should be made in `docs/source`. To preview
changes:

```bash
uv run nox -s docs_serve
```

The output of the above command provides a URL for viewing the documentation via a local server (usually [http://127.0.0.1:8000](http://127.0.0.1:8000)).

### Submitting code changes

After you've completed the changes described in the issue you're working on,
you can submit them by [creating a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request-from-a-fork) (PR) in the `pyprefab` repository.

Please ensure the following are true before creating the PR:

- Your change is covered by tests, if applicable
- Project documentation is updated, if applicable
- All nox checks pass: `uv run nox --tags checks`
- The `[Unreleased]` section of [CHANGELOG.md](CHANGELOG.md) contains a
description of your change.

The PR itself should:

- Have a descriptive title
- Be [linked to its corresponding issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)
in the description.
- Have a description that includes any other information or context that will
help a code reviewer understand your changes.
