import sys
import os
from common import exit_with_error

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(PATH, "..", "conf", "templates")


def import_user_module(module, exit=True):
    """
        Imports a user module
    """

    try:
        return __import__(module, locals(), globals(), [])

    except ImportError:

        if exit:
            exit_with_error("%s.py file not found!" % module)


def generate_template(tm_name, project_name, output_dir, new_extension=None):
    """
        Generates a project's file from a template
    """

    tm_name, ext = os.path.splitext(tm_name)
    if not ext:
        ext = ".tm"

    if new_extension is None:
        new_extension = '.py'

    with open(os.path.join(TEMPLATES_DIR, "%s%s" % (tm_name, ext)), 'r') as f:
        template = f.read()

    data = template % { 'project_name' : project_name }

    with open(os.path.join(output_dir, "%s%s" % (tm_name, new_extension)), 'w') as f:
        f.write(data)


def get_full_template_path(tm_name, extension=None):
    """
        Returns the full template path
    """

    if extension is None:
        extension = "tm"
    return os.path.join(TEMPLATES_DIR, "%s.%s" % (tm_name, extension))
