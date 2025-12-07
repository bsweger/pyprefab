"""Snapshot tests for pyprefab templates."""

import tomllib  # type: ignore

import pytest


def test_pyproject_docs(cli_output, snapshot):
    """pyproject.toml contents are correct for project with docs."""
    package_path, cli_result = cli_output
    with open(package_path / 'pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
    assert pyproject.get('dependency-groups', {}).get('docs')
    assert pyproject == snapshot


@pytest.mark.parametrize(
    'meta_file',
    [
        'CHANGELOG.md',
        'CONTRIBUTING.md',
        'LICENSE',
        'README.md',
    ],
)
def test_meta_files(cli_output, snapshot, meta_file):
    """Location and contents of CHANGELOG.md are correct."""
    package_path, cli_result = cli_output
    with open(package_path / meta_file, 'r', encoding='utf-8') as f:
        file_contents = f.read()
    assert file_contents == snapshot


@pytest.mark.parametrize(
    'docs_file',
    [
        'conf.py',
        'index.rst',
        'CHANGELOG.md',
        'CONTRIBUTING.md',
        'readme.md',
        'usage.md',
    ],
)
def test_docs_dir(cli_output, snapshot, docs_file):
    """Documentation contents are correct."""
    package_path, cli_result = cli_output
    with open(package_path / 'docs' / 'source' / docs_file, 'r', encoding='utf-8') as f:
        file = f.read()
    assert file == snapshot


def test_pyproject_no_docs(cli_output_no_docs, snapshot):
    """pyproject.toml contents are correct for project without docs."""
    package_path, cli_result = cli_output_no_docs
    with open(package_path / 'pyproject.toml', 'rb') as f:
        pyproject = tomllib.load(f)
    assert pyproject.get('dependency-groups', {}).get('docs') is None
    assert pyproject == snapshot


@pytest.mark.parametrize(
    'src_file',
    [
        '__init__.py',
        'app.py',
        'logger.py',
    ],
)
def test_src_dir(cli_output, snapshot, src_file):
    """Template files in src/ rendered correctly."""
    package_path, cli_result = cli_output
    with open(package_path / 'src' / 'transporter_logs' / src_file, 'r', encoding='utf-8') as f:
        file = f.read()
    assert file == snapshot


@pytest.mark.parametrize(
    'gh_workflow_file',
    [
        'ci.yaml',
        'publish-pypi.yaml',
    ],
)
def test_gh_workflows(cli_output, snapshot, gh_workflow_file):
    """Github workflow templates rendered correctly."""
    package_path, cli_result = cli_output
    with open(package_path / '.github' / 'workflows' / gh_workflow_file, 'r', encoding='utf-8') as f:
        file = f.read()
    assert file == snapshot
