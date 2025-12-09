import sys

from pyprefab.cli import app

rc = 1
try:
    app()
    rc = 0
except Exception as e:
    print("Error:", e, file=sys.stderr)
sys.exit(rc)
