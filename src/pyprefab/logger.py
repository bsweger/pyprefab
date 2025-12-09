import logging
import sys

import structlog


def configure_logging(config) -> None:
    # Set logging level from config if available
    log_level = config.get_package_setting("logging.level")
    if log_level is not None:
        logging.root.setLevel(log_level)

    shared_processors = [
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.add_log_level,
        structlog.processors.CallsiteParameterAdder([structlog.processors.CallsiteParameter.FILENAME]),
    ]

    if sys.stderr.isatty():
        # If we're in a terminal, pretty print the logs.
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(),
        ]  # pragma: no cover
    else:
        # Otherwise, output logs in JSON format
        processors = shared_processors + [
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.root.level),
        cache_logger_on_first_use=True,
    )
