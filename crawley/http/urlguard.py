"""SSRF guard — block fetches to private / internal network targets.

Server-side crawlers that follow user-supplied or discovered URLs are a classic
`SSRF <https://owasp.org/www-community/attacks/Server_Side_Request_Forgery>`_
vector: a link (or an HTTP redirect) can point at ``127.0.0.1``, a private
``10.0.0.0/8`` host, or the cloud metadata endpoint ``169.254.169.254`` and
exfiltrate secrets. This module rejects those targets.

The guard is **opt-in**. It is off unless :data:`crawley.config.SSRF_PROTECT`
(or a per-crawler ``SSRF_PROTECT`` setting) is truthy, so local development
against ``localhost`` keeps working by default. When enabled, the HTTP manager
installs an ``httpx`` request event-hook that runs :func:`current_guard` on
every request URL *including each redirect hop* (the hook only inspects the URL,
so it costs no extra connection).

Everything here is pure standard library (``ipaddress`` / ``socket`` /
``urllib``); the module has no third-party or framework dependencies. A
downstream application that already ships its own, stricter policy can install it
once with :func:`set_url_guard` and the manager will use it instead.
"""

import functools
import ipaddress
import socket
import urllib.parse
from typing import Callable

__all__ = [
    "UnsafeUrl",
    "is_safe_url",
    "assert_safe_url",
    "host_is_obviously_internal",
    "set_url_guard",
    "current_guard",
    "reset_url_guard",
    "BLOCKED_HOSTS",
]

#: Hostnames that must never be fetched, independent of DNS resolution — the
#: common cloud-metadata and loopback aliases.
BLOCKED_HOSTS = {
    "localhost",
    "metadata",
    "metadata.google.internal",
    "instance-data",
    "instance-data.ec2.internal",
}


class UnsafeUrl(ValueError):
    """Raised by :func:`assert_safe_url` when a URL is not a safe public target."""


def _ip_is_blocked(ip):
    """True if *ip* (a string) is anything other than a public, routable address."""
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return True  # unparseable -> treat as unsafe
    # ``is_global`` is the strict allow-test; the explicit flags are
    # belt-and-suspenders across Python versions / address families.
    if not addr.is_global:
        return True
    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
        or addr.is_unspecified
    )


def host_is_obviously_internal(host: str) -> bool:
    """No-DNS check: is *host* a literal internal IP or a known metadata name?

    Cheap, resolution-free screen for hot paths (e.g. a headless browser firing
    many sub-requests). It does **not** catch a DNS name that resolves to a
    private IP — pair it with :func:`is_safe_url` on the entry URL for that.

    Args:
        host: A bare hostname or IP literal (no scheme / port).

    Returns:
        ``True`` if the host is obviously internal and must not be fetched.
    """
    if not host:
        return True
    h = host.strip("[]").lower()
    if h in BLOCKED_HOSTS:
        return True
    # Only judge LITERAL IPs here; a DNS name is not "obviously" internal (that
    # is :func:`is_safe_url`'s job to resolve). NB: ``_ip_is_blocked`` treats any
    # non-IP string as blocked, so it must not be called on hostnames.
    try:
        ipaddress.ip_address(h)
    except ValueError:
        return False  # a hostname, e.g. example.com — allow
    return _ip_is_blocked(h)


@functools.lru_cache(maxsize=4096)
def _resolve_blocked(host, port):
    """Cached: ``True`` if *host* resolves to any blocked IP (or cannot resolve)."""
    try:
        infos = socket.getaddrinfo(host, port or 80, proto=socket.IPPROTO_TCP)
    except Exception:
        return True
    if not infos:
        return True
    return any(_ip_is_blocked(info[4][0]) for info in infos)


def is_safe_url(url: str) -> bool:
    """True if *url* is an ``http(s)`` URL that resolves only to public IPs.

    Rejects non-HTTP schemes, embedded ``user:pass@`` credentials (which can mask
    the real host from naive parsers), the :data:`BLOCKED_HOSTS` names, and any
    host that resolves — now — to a private, loopback, link-local, reserved,
    multicast or unspecified address. DNS results are cached (see
    :func:`_resolve_blocked`).

    Args:
        url: The absolute URL to test.

    Returns:
        ``True`` if the URL is safe to fetch, ``False`` otherwise.
    """
    try:
        parsed = urllib.parse.urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in ("http", "https"):
        return False
    if parsed.username or parsed.password:
        return False  # user:pass@ can mask the real host / confuse parsers
    host = parsed.hostname
    if not host or host.strip("[]").lower() in BLOCKED_HOSTS:
        return False
    return not _resolve_blocked(host, parsed.port)


def assert_safe_url(url: str) -> str:
    """Return *url* if safe, else raise :class:`UnsafeUrl`.

    Args:
        url: The absolute URL to test.

    Raises:
        UnsafeUrl: If *url* is not a safe public ``http(s)`` target.
    """
    if not is_safe_url(url):
        raise UnsafeUrl("Refusing to fetch non-public or non-HTTP URL: %s" % url)
    return url


# -- overridable guard ---------------------------------------------------------
#
# The HTTP manager calls ``current_guard()`` rather than ``is_safe_url`` directly
# so a host application can substitute its own policy (e.g. an allow-list, or a
# guard that also pins the resolved IP) exactly once at start-up.

_GUARD = is_safe_url


def set_url_guard(fn: Callable[[str], bool]) -> None:
    """Install *fn* as the active guard used by the HTTP layer.

    Args:
        fn: A callable ``(url: str) -> bool`` returning ``True`` for safe URLs.
    """
    global _GUARD
    if not callable(fn):
        raise TypeError("url guard must be callable (url: str) -> bool")
    _GUARD = fn


def current_guard() -> Callable[[str], bool]:
    """Return the active guard callable (the built-in :func:`is_safe_url` by default)."""
    return _GUARD


def reset_url_guard() -> None:
    """Restore the built-in :func:`is_safe_url` guard (mainly for tests)."""
    global _GUARD
    _GUARD = is_safe_url
