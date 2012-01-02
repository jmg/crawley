import os.path

from crawley.utils import generate_template
from crawley.simple_parser import Generator
from crawley.simple_parser.compilers import CrawlerCompiler

from base import BaseProject
from crawley.utils import generate_template, import_user_module
from crawley.simple_parser.config_parser import ConfigApp


class TemplateProject(BaseProject):
    """
        This class represents a template project.
        It can be started with:

            ~$ crawley startproject -t template [name]
    """

    name = "template"

    def set_up(self, project_name, **kwargs):
        """
            Setups a crawley's template project
        """

        BaseProject.set_up(self, project_name, **kwargs)

        self._generate_templates(project_name)

    def _generate_templates(self, project_name):

        generate_template("template", project_name, self.project_dir, new_extension=".crw")
        generate_template("config", project_name, self.project_dir, new_extension=".ini")

    def syncdb(self, syncb_command):
        """
            Builds the database
        """

        BaseProject.syncdb(self, syncb_command)

        if self.connector is None:
            return

        template = self._get_template(syncb_command)

        syncb_command.generator = Generator(template, syncb_command.settings)
        entities = syncb_command.generator.gen_entities()

        self._setup_entities(entities, syncb_command.settings)

    def _get_template(self, syncb_command):

        with open(os.path.join(syncb_command.settings.PROJECT_ROOT, "template.crw"), "r") as f:
            return f.read()

    def run(self, run_command):
        """
            Runs the crawley.

            For this kind of project it needs to generate the crawlers and scrapers
            classes at runtime first.
        """

        scraper_classes = run_command.syncdb.generator.gen_scrapers()

        config = self._get_config(run_command)

        compiler = CrawlerCompiler(scraper_classes, config)
        crawler_class = compiler.compile()

        BaseProject.run(self, run_command, [crawler_class])

    def _get_config(self, run_command):

        return ConfigApp(run_command.settings.PROJECT_ROOT)
