import logging

from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings, PyprojectTomlConfigSettingsSource, SettingsConfigDict


class LoggingConfig(BaseModel):
    """Logging configuration settings."""

    level: str = "INFO"

    @field_validator("level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        if not hasattr(logging, v):
            raise ValueError(f"Invalid logging level: {v}")
        return v


class PyprefabConfig(BaseSettings):
    """
    Manages pyprefab package configuration.

    Loads configuration from a TOML file with environment variable overrides.
    Environment variables take precedence over TOML values.

    Environment variable format: PYPREFAB_{SECTION}_{KEY}
    Example: PYPREFAB_LOGGING_LEVEL overrides the logging.level setting.
    """

    model_config = SettingsConfigDict(
        pyproject_toml_table_header=("tool", "pyprefab"),
        env_prefix="PYPREFAB_",
        env_nested_delimiter="_",
    )

    logging: LoggingConfig = LoggingConfig()

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        return (
            kwargs["env_settings"],
            PyprojectTomlConfigSettingsSource(settings_cls),
        )
