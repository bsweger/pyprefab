import structlog

from pyprefab.util.date import get_current_date
from pyprefab.util.logs import setup_logging

setup_logging()
logger = structlog.get_logger()


def main():
    """Application entry point."""

    today = get_current_date()
    logger.info('retrieved the date', date=today)

    return f'Hello, today is {today}!'


if __name__ == '__main__':
    main()