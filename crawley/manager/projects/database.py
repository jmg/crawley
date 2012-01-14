import os.path

from crawley.utils import generate_template
from crawley.simple_parser import Generator
from crawley.simple_parser.compilers import CrawlerCompiler

from template import TemplateProject
from crawley.utils import generate_template, import_user_module
from crawley.simple_parser.config_parser import ConfigApp


class DataBaseProject(TemplateProject):
    """
        This class represents a database project.
        It can be started with:

            ~$ crawley startproject -t database [name]
    """

    name = "database"

    def set_up(self, project_name, base_dir=None):
        """
            Setups a crawley database project
        """

        main_module = project_name

        if base_dir is not None:
            main_module = os.path.join(base_dir, project_name)

        self._create_module(main_module)
        self._write_meta_data(main_module)

    def _get_template(self, syncb_command):

        return syncb_command.kwargs["template"]

    def _get_config(self, run_command):

        return run_command.kwargs["config"]

