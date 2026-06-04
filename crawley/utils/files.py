"""Filesystem and settings helpers."""

import os


def check_for_file(settings, file_name):
    """Check if a project file exists."""
    return os.path.exists(os.path.join(settings.PROJECT_ROOT, file_name))


def fix_file_extension(file_name, extension):
    """Ensure *file_name* ends with ``.extension``."""
    if not file_name.endswith(".%s" % extension):
        file_name = "%s.%s" % (file_name, extension)
    return file_name


def has_valid_attr(settings, attr_name):
    """Return ``True`` if *settings* has a non-empty *attr_name* attribute."""
    attr = getattr(settings, attr_name, None)
    return attr is not None and bool(attr)


def get_settings_attribute(settings, attr_name, default=None):
    """Return *attr_name* from *settings* or *default* when missing/empty."""
    attr = getattr(settings, attr_name, None)
    if attr is None or not attr:
        return default
    return attr
