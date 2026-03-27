"""Test pyprefab app configuration."""

import pytest

from pyprefab.config import PyprefabConfig


def test_config_defaults():
    config = PyprefabConfig()
    assert config.logging.level == "INFO"


def test_config_env_override(monkeypatch):
    monkeypatch.setenv("PYPREFAB_LOGGING_LEVEL", "DEBUG")
    config = PyprefabConfig()
    assert config.logging.level == "DEBUG"


def test_validate_config(monkeypatch):
    """Invalid logging level should raise a config error."""
    monkeypatch.setenv("PYPREFAB_LOGGING_LEVEL", "INVALID_LEVEL")
    with pytest.raises(ValueError, match="Invalid logging level"):
        PyprefabConfig()
