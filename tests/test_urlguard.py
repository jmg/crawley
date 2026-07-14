"""Tests for the SSRF URL guard (:mod:`crawley.http.urlguard`).

Hermetic: only IP literals and the built-in blocked-host names are used, so
``socket.getaddrinfo`` never performs a real DNS query.
"""

import pytest

from crawley.http import urlguard


def test_blocks_loopback_private_and_metadata():
    assert not urlguard.is_safe_url("http://127.0.0.1/")
    assert not urlguard.is_safe_url("http://10.0.0.5/admin")
    assert not urlguard.is_safe_url("http://192.168.1.1/")
    assert not urlguard.is_safe_url("http://169.254.169.254/latest/meta-data/")
    assert not urlguard.is_safe_url("http://localhost:8000/")


def test_blocks_non_http_scheme_and_userinfo():
    assert not urlguard.is_safe_url("file:///etc/passwd")
    assert not urlguard.is_safe_url("ftp://8.8.8.8/")
    assert not urlguard.is_safe_url("gopher://8.8.8.8/")
    # user:pass@ can mask the real host from naive parsers.
    assert not urlguard.is_safe_url("http://user:pass@8.8.8.8/")


def test_allows_public_ip():
    # getaddrinfo on a numeric IP is resolved locally (no DNS query), so this
    # stays hermetic while exercising the "allow" path.
    assert urlguard.is_safe_url("http://8.8.8.8/")
    assert urlguard.is_safe_url("https://8.8.8.8/path?q=1")


def test_assert_safe_url():
    with pytest.raises(urlguard.UnsafeUrl):
        urlguard.assert_safe_url("http://127.0.0.1/")
    assert urlguard.assert_safe_url("http://8.8.8.8/") == "http://8.8.8.8/"


def test_host_is_obviously_internal():
    assert urlguard.host_is_obviously_internal("127.0.0.1")
    assert urlguard.host_is_obviously_internal("10.1.2.3")
    assert urlguard.host_is_obviously_internal("metadata.google.internal")
    assert urlguard.host_is_obviously_internal("")
    # A public IP literal and a bare hostname are not "obviously" internal.
    assert not urlguard.host_is_obviously_internal("8.8.8.8")
    assert not urlguard.host_is_obviously_internal("example.com")


def test_guard_registry_override_and_reset():
    assert urlguard.current_guard() is urlguard.is_safe_url
    urlguard.set_url_guard(lambda u: True)
    try:
        assert urlguard.current_guard()("http://127.0.0.1/") is True  # override wins
    finally:
        urlguard.reset_url_guard()
    assert urlguard.current_guard() is urlguard.is_safe_url


def test_set_url_guard_rejects_non_callable():
    with pytest.raises(TypeError):
        urlguard.set_url_guard(123)
    # a failed set must not corrupt the active guard
    assert urlguard.current_guard() is urlguard.is_safe_url
