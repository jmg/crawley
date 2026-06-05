"""HTTP layer for crawley."""

from crawley.http.managers import FastRequestManager, RequestManager
from crawley.http.response import Response

__all__ = ["RequestManager", "FastRequestManager", "Response"]
