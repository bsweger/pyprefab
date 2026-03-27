"""Test pyprefab app configuration."""

import pytest

from pyprefab.config import PyprefabConfig


def test_config_defaults(monkeypatch, tmp_path):
    """Field defaults apply when no pyproject.toml settings are present."""
    monkeypatch.chdir(tmp_path)
    config = PyprefabConfig()
    assert config.logging.level == "INFO"


def test_config_env_override(monkeypatch):
    """Config recognizes environment variable-based settings."""
    monkeypatch.setenv("PYPREFAB_LOGGING_LEVEL", "DEBUG")
    config = PyprefabConfig()
    assert config.logging.level == "DEBUG"


def test_config_pyproject_toml(monkeypatch, tmp_path):
    """Config recognizes settings in pyproject.toml."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[tool.pyprefab.logging]\nlevel = 'WARNING'\n")
    monkeypatch.chdir(tmp_path)
    config = PyprefabConfig()
    assert config.logging.level == "WARNING"


def test_validate_config(monkeypatch):
    """Invalid logging level should raise a config error."""
    monkeypatch.setenv("PYPREFAB_LOGGING_LEVEL", "INVALID_LEVEL")
    with pytest.raises(ValueError, match="Invalid logging level"):
        PyprefabConfig()
