"""The "template" (DSL) project type."""

import os.path

from crawley.manager.projects.base import BaseProject
from crawley.simple_parser import Generator
from crawley.simple_parser.compilers import CrawlerCompiler
from crawley.simple_parser.config_parser import ConfigApp
from crawley.utils import generate_template


class TemplateProject(BaseProject):
    """A project described with the crawley DSL.

    Created with::

        ~$ crawley startproject -t template [name]
    """

    name = "template"

    def set_up(self, project_name, **kwargs):
        super().set_up(project_name, **kwargs)
        self._generate_templates(project_name)

    def _generate_templates(self, project_name):
        generate_template(
            "template", project_name, self.project_dir, new_extension=".crw"
        )
        generate_template(
            "config", project_name, self.project_dir, new_extension=".ini"
        )

    def syncdb(self, syncb_command):
        super().syncdb(syncb_command)

        if self.connector is None:
            return

        template = self._get_template(syncb_command)
        syncb_command.generator = Generator(template, syncb_command.settings)
        syncb_command.generator.gen_entities()
        self._setup_entities(syncb_command.settings)

    def _get_template(self, syncb_command):
        with open(
            os.path.join(syncb_command.settings.PROJECT_ROOT, "template.crw"), "r"
        ) as f:
            return f.read()

    def run(self, run_command):
        scraper_classes = run_command.syncdb.generator.gen_scrapers()
        config = self._get_config(run_command)

        compiler = CrawlerCompiler(scraper_classes, config)
        crawler_class = compiler.compile()

        super().run(run_command, [crawler_class])

    def _get_config(self, run_command):
        return ConfigApp(run_command.settings.PROJECT_ROOT)
