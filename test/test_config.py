"""Test pyprefab app configuration."""

import pytest

from pyprefab.config import PyprefabConfig


@pytest.fixture
def setenv(monkeypatch):
    """Fixture to set environment variables."""
    monkeypatch.setenv('PYPREFAB_TESTY_LEVELS_GREETING', 'HOWDY')
    monkeypatch.setenv('PYPREFAB_LOGGING_LEVEL', 'DEBUG')
    yield


def test_config_prefix():
    config = PyprefabConfig()
    assert isinstance(config._config, dict)
    assert config.env_prefix == 'PYPREFAB'


def test_config_custom_prefix():
    config = PyprefabConfig(env_prefix='HOWDY')
    assert config.env_prefix == 'HOWDY'


def test_config_env_override(setenv):
    config = PyprefabConfig()
    assert config.get_package_setting('testy.levels.greeting') == 'HOWDY'
    assert config.get_package_setting('testy.levels') == {'greeting': 'HOWDY'}
    assert config.get_package_setting('testy') == {'levels': {'greeting': 'HOWDY'}}
    assert config.get_package_setting('logging.level') == 'DEBUG'
    assert config.get_package_setting('fakekey.mwahaha') is None


def test_validate_config(monkeypatch):
    """Invalid logging level should raise a config error."""
    monkeypatch.setenv('PYPREFAB_LOGGING_LEVEL', 'INVALID_LEVEL')
    with pytest.raises(ValueError, match='Invalid logging level'):
        PyprefabConfig()
