"""Common, dependency free helpers."""

import sys


def exit_with_error(error="Non specified error"):
    """Terminate crawley printing an error message."""
    print(error, file=sys.stderr)
    sys.exit(1)


def search_class(base_klass, entities_list, return_class=False):
    """Return the first subclass of *base_klass* found in *entities_list*."""
    for klass in entities_list:
        if issubclass(klass, base_klass) and klass is not base_klass:
            return klass
    return None


def add_to_path(path, index=0):
    """Add *path* to ``sys.path`` if it isn't there yet."""
    if path not in sys.path:
        sys.path.insert(index, path)
