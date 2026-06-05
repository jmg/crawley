"""URL matching helpers."""

import re

WILDCARD = "%"


def url_matcher(url, pattern):
    """Return ``True`` if *url* matches *pattern*.

    ``%`` works as a wildcard:

    * ``"%foo%"``  -> ``foo`` anywhere in the url
    * ``"foo%"``   -> the url starts with ``foo``
    * ``"%foo"``   -> the url ends with ``foo``
    * ``"foo"``    -> exact match
    """
    if pattern.startswith(WILDCARD) and pattern.endswith(WILDCARD):
        return matcher(pattern[1:-1], url, strict=False)
    elif pattern.endswith(WILDCARD):
        return matcher(pattern[:-1], url[: len(pattern) - 1])
    elif pattern.startswith(WILDCARD):
        return matcher(pattern[1:], url[-len(pattern) + 1 :])
    else:
        return matcher(pattern, url)


def matcher(pattern, url, strict=True):
    """Check whether *pattern* matches *url*."""
    if strict:
        return pattern == url
    return pattern in url


def complex_matcher(pattern, url, strict=True):
    """Regex based matcher."""
    match = re.search(pattern, url)

    if match is None:
        return url in pattern

    group = match.group(0)

    if strict:
        return group == url
    return group in url
