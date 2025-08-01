import sys

import structlog


def configure_logging():
    shared_processors = [
        structlog.processors.TimeStamper(fmt='iso', utc=True),
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
        cache_logger_on_first_use=True,
    )
