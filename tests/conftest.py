"""Pytest configuration — ensures custom_components is importable.

CI installs the full Home Assistant stack via requirements.txt so the
import chain works. Local developers without those deps see a clear
collection-time skip rather than a confusing aiohttp/paho-mqtt ImportError.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
