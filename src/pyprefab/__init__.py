"""pyprefab initialization."""

from importlib.metadata import PackageNotFoundError, version

from pyprefab.logger import configure_logging

# configure structlog
configure_logging()

try:
    __version__ = version('pyprefab')
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
