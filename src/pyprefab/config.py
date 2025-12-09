import logging
import os
import tomllib  # type: ignore
from pathlib import Path
from typing import Any


class PyprefabConfig:
    """
    Manages pyprefab package configuration.

    This class loads package configuration from a TOML file and also applies
    any environment variable overrides.
    """

    def __init__(self, env_prefix: str = "PYPREFAB"):
        self.env_prefix = env_prefix.upper()
        self._config: dict[str, Any] = {}

        self._load_config()
        self.validate_config()

    def _load_config(self) -> None:
        """
        Load config with precedence order:
        1. TOML file (lowest)
        2. Environment variables (highest)
        """
        self._load_config_toml()
        self._apply_env_overrides()

    def _load_config_toml(self) -> None:
        """Load pyprefab .toml config."""
        config_path = Path(__file__).parent / "config.toml"

        if config_path.exists():
            with open(config_path, "rb") as f:
                self._config = tomllib.load(f)
        else:
            self._config = {}

    def _apply_env_overrides(self) -> None:
        """
        Apply environment variable overrides.

        Environment variable format: {PREFIX}_{SECTION}_{KEY}
        Example: PYPREFAB_LOGGING_LEVEL overrides config['logging']['level']
        """
        prefix = f"{self.env_prefix}_"
        env_overrides = {key[len(prefix) :]: value for key, value in os.environ.items() if key.startswith(prefix)}

        if not env_overrides:
            return

        for env_key, env_value in env_overrides.items():
            config_path = [part.lower() for part in env_key.split("_")]

            # set config value
            self._set_nested_config_value(config_path, env_value)

    def _set_nested_config_value(self, config_path: list[str], env_value: str) -> None:
        """
        Update self._config with a nested value from a config path.

        Args:
            config_path: List of keys representing the path in the config
            env_value: String value to set at the deepest level

        Example:
            _set_nested_config_value(['logging', 'level'], 'DEBUG')
            updates self._config['logging']['level'] = 'DEBUG'
        """
        if not config_path:
            return

        current = self._config
        for key in config_path[:-1]:
            if key not in current:
                current[key] = {}
            elif not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]

        current[config_path[-1]] = env_value

    def get_package_setting(self, key: str, default=None):
        """Get pyprefab package settings."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def validate_config(self):
        """Validate the loaded configuration."""
        if not isinstance(self._config, dict):
            raise ValueError("Configuration must be a dictionary.")

        log_level = self.get_package_setting("logging.level")

        # check for valid logging level
        if log_level is not None and not hasattr(logging, log_level):
            raise ValueError(f"Invalid logging level: {log_level}")

        return True
