import sys

import structlog

from pyprefab.cli import app

logger = structlog.get_logger()

rc = 1
try:
    app()
    rc = 0
except Exception as e:
    logger.exception(the_error=e)
    print("Error:", e, file=sys.stderr)
sys.exit(rc)
