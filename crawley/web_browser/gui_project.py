import os

from crawley.extractors import PyQueryExtractor

from crawley.manager.commands.startproject import StartProjectCommand
from crawley.manager.commands.run import RunCommand
from crawley.manager.projects.template import TemplateProject
from config import SELECTED_CLASS

PATH = os.path.dirname(os.path.abspath(__file__))


class GUIProject(object):
    
    def __init__(self, dir_name, url):
        
        self.dir_name = dir_name
        self.url = url
    
    def set_up(self):
                
        dir_name, self.project_name = os.path.split(self.dir_name)
        os.chdir(dir_name)
        
        cmd = StartProjectCommand(project_type=TemplateProject.name, project_name=self.project_name)
        cmd.execute()
        
    def generate_teplate(self, html):
        
        obj = PyQueryExtractor().get_object(html)
        elements = obj(".%s" % SELECTED_CLASS)

        elements_xpath = [e.get("id") for e in elements]
        
        stream = "PAGE => %s \r\n" % self.url
        for i, e in enumerate(elements_xpath):
            stream += "%s.%s -> %s <br/>" % ("my_table", "my_field_%s" % i, e)

        with open(os.path.join(os.getcwd(), self.project_name, self.project_name, "template.crw"), "w") as f:
            f.write(stream.replace("<br/>", "\r\n"))

        os.sys.path.insert(0, self.project_name)        
        
    def run(self):
        
        import settings
        cmd = RunCommand(settings=settings)
        cmd.checked_execute()
