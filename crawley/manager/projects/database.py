"""The "database" project type (DSL template living next to a settings file)."""

import os.path

from crawley.manager.projects.template import TemplateProject


class DataBaseProject(TemplateProject):
    """A template project whose template/config are provided at runtime.

    Created with::

        ~$ crawley startproject -t database [name]
    """

    name = "database"

    def set_up(self, project_name, base_dir=None):
        main_module = project_name
        if base_dir is not None:
            main_module = os.path.join(base_dir, project_name)

        self._create_module(main_module)
        self._write_meta_data(main_module)

    def _get_template(self, syncb_command):
        return syncb_command.kwargs["template"]

    def _get_config(self, run_command):
        return run_command.kwargs["config"]
