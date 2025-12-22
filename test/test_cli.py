"""Test the pyprefab cli."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest
from click import unstyle
from typer.testing import CliRunner

import pyprefab
from pyprefab.cli import (
    app,  # type: ignore
    validate_author_desc,
    validate_package_name,
)
from pyprefab.exceptions import PyprefabBadParameter


@pytest.mark.parametrize(
    "package_name, expected_result",
    [
        ("valid_package_name", "valid_package_name"),
        ("valid_package_name123", "valid_package_name123"),
        ("AnnoyingButValid", "AnnoyingButValid"),
    ],
)
def test_valid_package_name(package_name, expected_result):
    """Test package name validation."""
    assert validate_package_name(package_name) == expected_result


@pytest.mark.parametrize(
    "package_name",
    [
        ("invalid-package-name"),
        ("invalid-package-name!"),
        ("1invalid_package_name"),
    ],
)
def test_invalid_package_name(package_name):
    """Test package name validation."""
    with pytest.raises(PyprefabBadParameter):
        validate_package_name(package_name)


@pytest.mark.parametrize(
    "author_name",
    [
        ('"double quote" not allowed"'),
        ('"'),
    ],
)
def test_invalid_author(author_name):
    """Test author name and package description name validation."""
    with pytest.raises(PyprefabBadParameter):
        validate_author_desc(author_name)


@pytest.mark.parametrize(
    "cli_inputs, expected_dirs",
    [
        (["--name", "pytest_package", "--author", "Py Test"], [".github", "src", "test"]),
        (["--name", "pytest_package", "--author", "Py Test", "--docs"], [".github", "docs", "src", "test"]),
    ],
)
def test_pyprefab_cli(tmp_path, cli_inputs, expected_dirs):
    runner = CliRunner()
    package_dir = tmp_path / "test_cli"

    result = runner.invoke(
        app,
        cli_inputs + ["--dir", package_dir],
        input="''\nn\n",
    )
    assert result.exit_code == 0
    assert package_dir.exists()

    # package directory populated with template output contains expected folders
    dir_count = 0
    dir_names = []
    for child in package_dir.iterdir():
        if child.is_dir():
            dir_names.append(child.name)
            dir_count += 1
    assert dir_count == len(expected_dirs)
    assert set(dir_names) == set(expected_dirs)


def test_version_param():
    """Version param runs eagerly and exits."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "bad-package-name!", "--version"],
    )
    assert result.exit_code == 0
    assert unstyle(result.stdout).strip() == f"pyprefab {pyprefab.__version__}"


def test_app_invalid_package_name(tmp_path):
    """Package name must be a valid Python identifier."""
    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "pytest-package", "--author", "Py Test", "--dir", tmp_path],
        input="This is a test package\n",
    )
    assert result.exit_code != 0


def test_app_package_dir_callback(monkeypatch, tmp_path):
    """App should fail if supplied package_dir is reserved."""
    # override the current home directory (for testing ~, etc.)
    envs = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}
    monkeypatch.setattr(os, "environ", envs)

    package_dir = "~/test_package_dir"
    runner = CliRunner()
    # boolean prompts require explicit 'n' or 'y'
    result = runner.invoke(
        app, ["--name", "pytest_package", "--author", "Py Test", "--dir", package_dir], input="''\nn\n"
    )
    assert result.exit_code == 0


def test_app_package_dir_file(monkeypatch, tmp_path):
    """App should fail if supplied package_dir is a file."""
    # override the current home directory (for testing ~, etc.)
    envs = {"HOME": str(tmp_path), "USERPROFILE": str(tmp_path)}
    monkeypatch.setattr(os, "environ", envs)

    # set up test by creating an existing file
    package_dir = "~/../test_package_dir//textfile.txt"
    normalized_dir = Path(package_dir).expanduser().resolve()
    normalized_dir.parent.mkdir(parents=True, exist_ok=True)
    normalized_dir.touch()

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "pytest_package", "--author", "Py Test", "--dir", package_dir],
        input="This is a test package\n",
    )
    assert result.exit_code != 0


def test_error_cleanup(tmp_path):
    """Error when creating a package should trigger cleanup."""
    package_dir = tmp_path / "test_error"
    with patch("pyprefab.cli.render_templates", side_effect=Exception("Test exception")):
        runner = CliRunner()
        result = runner.invoke(
            app,
            ["--name", "pytest_package", "--description", "", "--dir", package_dir],
            input="Py Test\n",
        )
    assert result.exit_code != 0
    # pyprefab should remove package directory if an error occurs
    assert package_dir.exists() is False


def test_error_existing_data(tmp_path):
    """If there are existing files in package directory, pyprefab should fail."""

    package_dir = tmp_path / "test_existing_data"
    package_dir.mkdir()
    (package_dir / "existing_file.txt").touch()

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "pytest_package", "--author", "Py Test", "--description", "new package", "--dir", package_dir],
        input="y\n",
    )
    assert result.exit_code != 0


def test_existing_data_exception(tmp_path):
    """If existing files in package directory are on the exception list, pyprefab should create the package."""

    package_dir = tmp_path / "test_existing_data"
    (package_dir / ".git").mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "pytest_package", "--author", "Py Test", "--description", "new package", "--dir", package_dir],
        input="y\n",
    )
    assert result.exit_code == 0


def test_existing_data_exception_and_no_exception(tmp_path):
    """If there's a mix of allowed and not allowed existing files in the package directory, pyprefab should fail."""

    package_dir = tmp_path / "test_existing_data"
    (package_dir / ".git").mkdir(parents=True, exist_ok=True)
    (package_dir / "logs").mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(
        app,
        ["--name", "pytest_package", "--author", "Py Test", "--description", "new package", "--dir", package_dir],
        input="y\n",
    )
    assert result.exit_code != 0


@pytest.mark.parametrize(
    "cli_inputs, expected_author",
    [
        (["--name", "pytest_package", "--author", "Authorin'' with many 'names 🧐", "--description", "testy"], "Authorin'' with many 'names 🧐"),
        (["--name", "pytest_package", "--author", "Author, Name", "--description", "testy"], "Author, Name"),
        (["--name", "pytest_package", "--author", "'", "--description", "testy"], "'"),
        (["--name", "pytest_package", "--author", "''", "--description", "testy"], "''"),
    ],
)
def test_pyprefab_author_names(tmp_path, cli_inputs, expected_author):
    """Author name should not be auto-escaped in jinja templates."""
    package_name = "pytest_package"
    runner = CliRunner()
    package_path = tmp_path / package_name
    result = runner.invoke(
        app,
        cli_inputs + ["--dir", package_path],
        input="y\n",
    )
    assert result.exit_code == 0
    with open(package_path / "pyproject.toml", "r", encoding="utf-8") as f:
        file = f.read()
        assert f'authors = [{{name = "{expected_author}"}}]' in file


@pytest.mark.parametrize(
    "cli_inputs, expected_description",
    [
        (["--name", "pytest_package", "--author", "Worf", "--description", "app for trackin' things"], "app for trackin' things"),
        (["--name", "pytest_package", "--author", "Worf", "--description", "''''"], "''''"),
        (["--name", "pytest_package", "--author", "Worf", "--description", "look ma, usin' an em dash: ⎯"], "look ma, usin' an em dash: ⎯"),
    ],
)

def test_pyprefab_description(tmp_path, cli_inputs, expected_description):
    """Author name should not be auto-escaped in jinja templates."""
    package_name = "pytest_package"
    runner = CliRunner()
    package_path = tmp_path / package_name
    result = runner.invoke(
        app,
        cli_inputs + ["--dir", package_path],
        input="y\n",
    )
    assert result.exit_code == 0
    with open(package_path / "pyproject.toml", "r", encoding="utf-8") as f:
        file = f.read()
        assert f'description = "{expected_description}"' in file
