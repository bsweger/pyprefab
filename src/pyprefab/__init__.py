"""pyprefab initialization."""

import sys
from importlib.metadata import PackageNotFoundError, version

from pyprefab.config import PyprefabConfig
from pyprefab.logger import configure_logging

# get application config
try:
    CONFIG = PyprefabConfig()
except ValueError as e:
    sys.exit(f'Invalid pyprefab configuration: {e}')

# configure structlog
configure_logging(CONFIG)

try:
    __version__ = version('pyprefab')
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
