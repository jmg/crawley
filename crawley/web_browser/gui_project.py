import os

from crawley.extractors import PyQueryExtractor

from crawley.manager.commands.startproject import StartProjectCommand
from crawley.manager.commands.run import RunCommand
from crawley.manager.projects.template import TemplateProject
from config import SELECTED_CLASS


class GUIProject(object):
    """
        A class that represents a crawley GUI project on the browser.
    """
    
    HEADER_LINE = "PAGE => %s \r\n"
    SENTENCE_LINE = "%s.%s -> %s \r\n"
    
    def __init__(self, dir_name, url):
                
        self.dir_name, self.project_name = os.path.split(dir_name)
        self.url = url
    
    def set_up(self, is_new=False):
        """
            Starts or opens a crawley's project depending on
            the [is_new] parameter
        """        
                                
        os.chdir(self.dir_name)
        os.sys.path.insert(0, self.project_name)
        
        if is_new:
            cmd = StartProjectCommand(project_type=TemplateProject.name, project_name=self.project_name)
            cmd.execute()
        
    def generate_template(self, html):
        """
            Generates a template based on what users selects
            on the browser.
        """        
        
        obj = PyQueryExtractor().get_object(html)
        elements = obj(".%s" % SELECTED_CLASS)

        elements_xpath = [e.get("id") for e in elements]
        
        stream = self.HEADER_LINE % self.url
        for i, e in enumerate(elements_xpath):
            stream += self.SENTENCE_LINE % ("my_table", "my_field_%s" % i, e)

        with open(os.path.join(os.getcwd(), self.project_name, self.project_name, "template.crw"), "w") as f:
            f.write(stream)
        
    def run(self):
        """
            Runs the crawler of the generated project 
        """
        
        import settings
        cmd = RunCommand(settings=settings)        
        cmd.checked_execute()
