"""Utility helpers re-exported for convenience."""

from crawley.utils.collections import CustomDict, OrderedDict
from crawley.utils.common import add_to_path, exit_with_error, search_class
from crawley.utils.files import (
    check_for_file,
    fix_file_extension,
    get_settings_attribute,
    has_valid_attr,
)
from crawley.utils.matchers import complex_matcher, matcher, url_matcher
from crawley.utils.projects import (
    generate_template,
    get_full_template_path,
    import_from_path,
    import_user_module,
)

__all__ = [
    "CustomDict",
    "OrderedDict",
    "add_to_path",
    "exit_with_error",
    "search_class",
    "check_for_file",
    "fix_file_extension",
    "get_settings_attribute",
    "has_valid_attr",
    "complex_matcher",
    "matcher",
    "url_matcher",
    "generate_template",
    "get_full_template_path",
    "import_from_path",
    "import_user_module",
]
