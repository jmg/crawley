from re import search
from UserDict import DictMixin

"""Utilities module"""

def url_matcher(url, pattern):
    """
        Returns True if the url matches the given pattern
    """

    WILDCARD = "%"

    if pattern.startswith(WILDCARD) and pattern.endswith(WILDCARD):
        return matcher(pattern[1:-1], url, strict=False)
    elif pattern.endswith(WILDCARD):
        return matcher(pattern[:-1], url[:len(pattern)-1])
    elif pattern.startswith(WILDCARD):
        return matcher(pattern[1:], url[-len(pattern)+1:])
    else:
        return matcher(pattern, url)


def matcher(pattern, url, strict=True):
    """
        Checks if the pattern matches the url
    """

    if strict:
        return pattern == url
    return pattern in url


def complex_matcher(pattern, url, strict=True):

    #FIXME
    match = search(pattern, url)

    if match is None:

        return url in pattern

    group = match.group(0)

    if strict:
        return group == url

    return group in url


class OrderedDict(DictMixin):
    """
        Ordered dict. Deprecated when we migrate to python 3
    """

    def __init__(self):
        self._keys = []
        self._data = {}

    def __setitem__(self, key, value):
        if key not in self._data:
            self._keys.append(key)
        self._data[key] = value

    def __getitem__(self, key):
        return self._data[key]

    def __delitem__(self, key):
        del self._data[key]
        self._keys.remove(key)

    def keys(self):
        return list(self._keys)

