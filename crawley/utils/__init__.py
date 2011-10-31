from collections import OrderedDict, CustomDict
from matchers import url_matcher, matcher
from common import exit_with_error, search_class
from projects import import_user_module,  generate_template, get_full_template_path
from files import check_for_file, fix_file_extension, has_valid_attr, get_settings_attribute
