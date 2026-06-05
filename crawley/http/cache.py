"""On-disk HTTP cache (a development helper).

Caches responses on disk keyed by *method + url + body* so repeated runs don't
hit the site again. Enable it on a crawler/spider with ``http_cache = True``.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Any, Optional


class _CachedResponse:
    """Minimal stand-in exposing ``status_code`` and ``headers``."""

    def __init__(self, status_code: Optional[int], headers: Optional[dict]) -> None:
        self.status_code = status_code
        self.headers = headers or {}


class HttpCache:
    """A tiny JSON-on-disk response cache."""

    def __init__(self, cache_dir: str = ".crawley_cache", enabled: bool = True) -> None:
        self.cache_dir = cache_dir
        self.enabled = enabled

    @staticmethod
    def _normalize(data: Any) -> str:
        if data is None:
            return ""
        if isinstance(data, dict):
            return json.dumps(data, sort_keys=True)
        return str(data)

    def _key(self, method: str, url: str, data: Any) -> str:
        raw = "%s|%s|%s" % (method.upper(), url, self._normalize(data))
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def _path(self, key: str) -> str:
        return os.path.join(self.cache_dir, key + ".json")

    def get(self, method: str, url: str, data: Any = None) -> Optional[dict]:
        if not self.enabled:
            return None
        path = self._path(self._key(method, url, data))
        if not os.path.isfile(path):
            return None
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def store(
        self,
        method: str,
        url: str,
        data: Any,
        status_code: Optional[int],
        final_url: str,
        headers: Any,
        body: str,
    ) -> None:
        if not self.enabled:
            return
        os.makedirs(self.cache_dir, exist_ok=True)
        payload = {
            "status": status_code,
            "url": final_url,
            "headers": dict(headers or {}),
            "body": body,
        }
        with open(self._path(self._key(method, url, data)), "w", encoding="utf-8") as f:
            json.dump(payload, f)
