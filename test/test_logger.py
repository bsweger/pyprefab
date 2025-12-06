"""Test pyprefab logger configuration."""

import logging
from unittest import mock

import pytest
import structlog

from pyprefab.logger import configure_logging


@pytest.fixture
def reset_logging():
    """Reset logging configuration after each test."""
    yield
    # reset to default WARNING level and clear struclog config
    logging.root.setLevel(logging.WARNING)
    structlog.reset_defaults()


def test_logging_level_from_config(reset_logging, monkeypatch):
    """Test that logging level is set from config when specified."""
    monkeypatch.setenv('PYPREFAB_LOGGING_LEVEL', 'DEBUG')
    configure_logging()

    assert logging.root.level == logging.DEBUG


def test_logging_level_default_when_not_specified(reset_logging, monkeypatch):
    """Test that logging level uses Python's default WARNING when not specified."""
    monkeypatch.delenv('PYPREFAB_LOGGING_LEVEL', raising=False)

    # mock the config to return None for logging.level
    with mock.patch('pyprefab.logger.PyprefabConfig') as mock_config:
        mock_instance = mock_config.return_value
        mock_instance.get_package_setting.return_value = None
        configure_logging()

        assert logging.root.level == logging.WARNING
