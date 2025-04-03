"""Test the pyprefab cli."""

from unittest.mock import patch

import pytest
from typer.testing import CliRunner

from pyprefab.cli import app  # type: ignore


@pytest.mark.parametrize(
    'cli_inputs, expected_dirs',
    [
        (['--name', 'pytest_project', '--author', 'Py Test'], ['.github', 'src', 'test']),
        (['--name', 'pytest_project', '--author', 'Py Test', '--docs'], ['.github', 'docs', 'src', 'test']),
    ],
)
def test_pyprefab_cli(tmp_path, cli_inputs, expected_dirs):
    runner = CliRunner()
    project_dir = tmp_path / 'test_cli'

    result = runner.invoke(
        app,
        cli_inputs + ['--dir', project_dir],
        input='""\n',
    )
    assert result.exit_code == 0
    assert project_dir.exists()

    # project directory populated with template output contains expected folders
    dir_count = 0
    dir_names = []
    for child in project_dir.iterdir():
        if child.is_dir():
            dir_names.append(child.name)
            dir_count += 1
    assert dir_count == len(expected_dirs)
    assert set(dir_names) == set(expected_dirs)


def test_invalid_project_name(tmp_path):
    """Project name must be a valid Python identifier."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest-project', '--author', 'Py Test', '--dir', tmp_path],
        input='This is a test project\n',
    )
    assert result.exit_code != 0


def test_error_cleanup(tmp_path):
    """Error when creating a project should trigger cleanup."""
    project_dir = tmp_path / 'test_error'
    with patch('pyprefab.cli.render_templates', side_effect=Exception('Test exception')):
        runner = CliRunner()
        result = runner.invoke(
            app,
            ['--name', 'pytest_project', '--description', '', '--dir', project_dir],
            input='Py Test\n',
        )
    assert result.exit_code != 0
    # pyprefab should remove project directory if an error occurs
    assert project_dir.exists() is False


def test_error_existing_data(tmp_path):
    """If there are existing files in project directory, pyprefab should fail."""

    project_dir = tmp_path / 'test_existing_data'
    project_dir.mkdir()
    (project_dir / 'existing_file.txt').touch()

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_project', '--author', 'Py Test', '--description', 'new project', '--dir', project_dir],
        input='y\n',
    )
    assert result.exit_code != 0


def test_existing_data_exception(tmp_path):
    """If existing files in project directory are on the exception list, pyprefab should create the package."""

    project_dir = tmp_path / 'test_existing_data'
    (project_dir / '.git').mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_project', '--author', 'Py Test', '--description', 'new project', '--dir', project_dir],
        input='y\n',
    )
    assert result.exit_code == 0


def test_existing_data_exception_and_no_exception(tmp_path):
    """If there's a mix of allowed and not allowed existing files in project directory, pyprefab should fail."""

    project_dir = tmp_path / 'test_existing_data'
    (project_dir / '.git').mkdir(parents=True, exist_ok=True)
    (project_dir / 'logs').mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ['--name', 'pytest_project', '--author', 'Py Test', '--description', 'new project', '--dir', project_dir],
        input='y\n',
    )
    assert result.exit_code != 0
