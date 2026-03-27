"""Test pyprefab logger configuration."""

import logging

import pytest
import structlog

from pyprefab.config import PyprefabConfig
from pyprefab.logger import configure_logging


@pytest.fixture
def reset_logging(monkeypatch):
    """Reset logging configuration before and after each test."""
    # clear existing logging level env var and reset to default of WARNING
    monkeypatch.delenv("PYPREFAB_LOGGING_LEVEL", raising=False)
    logging.root.setLevel(logging.WARNING)

    yield

    # clean up after test
    logging.root.setLevel(logging.WARNING)
    structlog.reset_defaults()


def test_logging_level_from_config(reset_logging, monkeypatch):
    """Logging level env variable should override other config sources."""
    monkeypatch.setenv("PYPREFAB_LOGGING_LEVEL", "DEBUG")
    config = PyprefabConfig()
    configure_logging(config)

    assert logging.root.level == logging.DEBUG


def test_logging_level_default_when_not_specified(reset_logging, monkeypatch, tmp_path):
    """Logging level should use field default (INFO) when no config sources are present."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("PYPREFAB_LOGGING_LEVEL", raising=False)
    config = PyprefabConfig()
    configure_logging(config)
    assert logging.root.level == logging.INFO
