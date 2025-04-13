"""pyprefab initialization."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('pyprefab')
except PackageNotFoundError:  # pragma: no cover
    # package is not installed
    pass
