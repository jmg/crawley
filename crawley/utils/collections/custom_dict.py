"""A dict that fails loudly on missing keys."""

from crawley.utils.common import exit_with_error


class CustomDict(dict):
    """A dict that terminates the program when a key is missing."""

    def __init__(self, error="[%s] Not valid argument", *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        if key in self:
            return dict.__getitem__(self, key)
        exit_with_error(self.error % key)
