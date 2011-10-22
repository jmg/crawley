import os.path

from crawley.manager.utils import generate_template
from crawley.simple_parser import interprete
from crawley.simple_parser.compilers import CrawlerCompiler
from crawley.persistance import session

from base import BaseProject
from crawley.manager.utils import generate_template, import_user_module


class TemplateProject(BaseProject):
    """
        This class represents a template project.
        It can be started with:

            ~$ crawley startproject -t template [name]
    """

    name = "template"

    def set_up(self, project_name):
        """
            Setups a crawley's template project
        """

        BaseProject.set_up(self, project_name)

        generate_template("template", project_name, self.project_dir, new_extension=".crw")
        generate_template("config", project_name, self.project_dir, new_extension=".ini")

    def syncdb(self, syncb_command):
        """
            Builds the database
        """

        with open(os.path.join(syncb_command.settings.PROJECT_ROOT, "template.crw"), "r") as f:
            template = f.read()

        syncb_command.scraper_classes = interprete(template, syncb_command.settings)

    def run(self, run_command):
        """
            Runs the crawley.

            For this kind of project it needs to generate the crawlers and scrapers
            classes at runtime first.
        """

        compiler = CrawlerCompiler(run_command.syncdb.scraper_classes, run_command.settings)
        crawler_class = compiler.compile()

        global session
        sessions = [session]
        crawler = crawler_class(sessions=sessions, debug=run_command.settings.SHOW_DEBUG_INFO)
        crawler.start()

        for session in sessions:
            session.close()

