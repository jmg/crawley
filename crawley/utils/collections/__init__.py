"""Collection helpers.

``OrderedDict`` used to be a backport for Python 2; on Python 3 the stdlib
implementation is re-exported for backwards compatibility.
"""

from collections import OrderedDict

from crawley.utils.collections.custom_dict import CustomDict

__all__ = ["OrderedDict", "CustomDict"]
