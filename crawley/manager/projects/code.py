"""The "code" project type."""

from crawley.crawlers import user_crawlers
from crawley.manager.projects.base import BaseProject
from crawley.utils import generate_template, import_user_module


class CodeProject(BaseProject):
    """A project whose crawlers/models are written by hand in Python.

    Created with::

        ~$ crawley startproject -t code [name]
    """

    name = "code"

    def set_up(self, project_name, **kwargs):
        super().set_up(project_name, **kwargs)
        generate_template("models", project_name, self.project_dir)
        generate_template("crawlers", project_name, self.project_dir)

    def syncdb(self, syncb_command):
        super().syncdb(syncb_command)
        if self.connector is not None:
            self._setup_entities(syncb_command.settings)

    def run(self, run_command):
        import_user_module("crawlers")
        super().run(run_command, user_crawlers)
