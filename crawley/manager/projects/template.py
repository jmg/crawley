from crawley.manager.utils import generate_template

from base import BaseProject


class TemplateProject(BaseProject):
    
    name = "template"
    
    def set_up(self, project_name):
        
        BaseProject.set_up(self, project_name)
        
        generate_template("template.py", project_name, project_name)
        
    def syncdb(self, syncb_command):
        
        with open("template.py", "r") as f:
            template = f.read()
        
        scraper_class = interprete(template, "name", syncb_command.settings)                
                        
        scraper_class
