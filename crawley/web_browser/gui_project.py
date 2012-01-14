import os

from crawley.extractors import PyQueryExtractor

from crawley.manager.commands.startproject import StartProjectCommand
from crawley.manager.commands.run import RunCommand
from crawley.manager.projects.template import TemplateProject
from crawley.exceptions import InvalidProjectError
from crawley.manager.utils import import_user_module
from crawley.simple_parser.config_parser import ConfigApp
from crawley.simple_parser.parsers import DSLAnalizer
from config import SELECTED_CLASS


class GUIProject(object):
    """
        A class that represents a crawley GUI project on the browser.
    """

    HEADER_LINE = "PAGE => %s \r\n"
    SENTENCE_LINE = "%s.%s -> %s \r\n"

    def __init__(self, dir_name):

        self.dir_name, self.project_name = os.path.split(dir_name)

    def set_up(self, browser_tab, is_new=False):
        """
            Starts or opens a crawley's project depending on
            the [is_new] parameter
        """

        os.chdir(self.dir_name)
        os.sys.path[0] = self.project_name

        if is_new:
            cmd = StartProjectCommand(project_type=TemplateProject.name, project_name=self.project_name)
            cmd.execute()

        else:
            self._validate_project()
            self._load_data(browser_tab)

        self.settings = import_user_module("settings")

    def _validate_project(self):
        """
            Checks if the given directory is a valid crawley project
        """

        try:
            with open(os.path.join(self.dir_name, self.project_name, "__init__.py"), "r") as f:
                content = f.read()

            if not 'crawley_version' in content:
                raise IOError
            if not 'template' in content:
                raise InvalidProjectError("The selected directory isn't a correct crawley project type")

        except IOError:
            raise InvalidProjectError("The selected directory isn't a crawley project")

    def _load_data(self, browser_tab):
        """
            Loads the project data into the browser
        """

        with open(os.path.join(self._get_project_path(), "template.crw"), "r") as f:
            template_data = f.read()

        analizer = DSLAnalizer(template_data)
        blocks = analizer.parse()

        for block in blocks:

            header = block[0]
            selected_nodes = [sentence.xpath for sentence in block[1:]]

            browser_tab.parent.tb_url.setText(header.xpath)
            browser_tab.load_url(header.xpath, selected_nodes=selected_nodes)

    def _get_project_path(self):
        """
            Returns the config.ini path
        """

        return os.path.join(self.dir_name, self.project_name, self.project_name)

    def get_configuration(self):
        """
            Returns the content of the config.ini
        """

        return ConfigApp(self._get_project_path())

    def generate_template(self, url, html):
        """
            Generates a template based on what users selects
            on the browser.
        """

        obj = PyQueryExtractor().get_object(html)
        elements = obj(".%s" % SELECTED_CLASS)

        elements_xpath = [e.get("id") for e in elements]

        stream = self.HEADER_LINE % url
        for i, e in enumerate(elements_xpath):
            stream += self.SENTENCE_LINE % ("my_table", "my_field_%s" % i, e)

        with open(os.path.join(os.getcwd(), self.project_name, self.project_name, "template.crw"), "w") as f:
            f.write(stream)

    def run(self):
        """
            Runs the crawler of the generated project
        """

        os.chdir(os.path.join(self.dir_name, self.project_name))

        cmd = RunCommand(settings=self.settings)
        cmd.checked_execute()
