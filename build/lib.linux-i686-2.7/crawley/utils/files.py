import os

def check_for_file(settings, file_name):
    """
        Checks if a project file exists
    """

    return os.path.exists(os.path.join(settings.PROJECT_ROOT, file_name))


def fix_file_extension(file_name, extension):
    """
        Fixes the file extensions
    """

    if not file_name.endswith(".%s" % extension):
        file_name = "%s.%s" % (file_name, extension)
    return file_name


def has_valid_attr(settings, attr_name):
    """
        Checks if settings has the attribute [attr_name] and it's not an empty string.
    """

    attr = getattr(settings, attr_name, None)
    return attr is not None and attr


def get_settings_attribute(settings, default=None):

    attr = getattr(settings, attr_name, None)
    return attr is not None and attr
