import os
import elixir
from multiprocessing import Process

from crawley.persistance import Entity, UrlEntity, setup
from crawley.persistance.connectors import connectors

from crawley.persistance import UrlEntity

from crawley.utils import import_user_module, search_class, generate_template
from crawley.crawlers import user_crawlers

from base import BaseProject


class CodeProject(BaseProject):
    """
        This class represents a code project.
        It can be started with:

            ~$ crawley startproject -t code [name]
    """

    name = "code"

    def set_up(self, project_name):
        """
            Setups a code project.
            Generates the crawlers and models files based on a template.
        """

        BaseProject.set_up(self, project_name)

        generate_template("models", project_name, self.project_dir)
        generate_template("crawlers", project_name, self.project_dir)

    def syncdb(self, syncb_command):
        """
            Builds the database and find the documents storages.
            Foreach storage it adds a session to commit the results.
        """

        BaseProject.syncdb(self, syncb_command)

        if self.connector is not None:
            self._setup_entities(elixir.entities, syncb_command.settings)

    def run(self, run_command):
        """
            Run the crawler of a code project
        """

        import_user_module("crawlers")
        BaseProject.run(self, run_command, user_crawlers)

