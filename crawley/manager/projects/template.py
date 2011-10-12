from crawley.manager.utils import generate_template
from crawley.simple_parser import interprete
from crawley.simple_parser.compilers import CrawlerCompiler 

from base import BaseProject
from crawley.manager.utils import generate_template


class TemplateProject(BaseProject):
    
    name = "template"
    
    def set_up(self, project_name):
        
        BaseProject.set_up(self, project_name)
                
        generate_template("template", project_name, project_name)
        generate_template("config", project_name, project_name)
        
    def syncdb(self, syncb_command):
        
        with open(os.path.join(syncb_command.settings.PROJECT_ROOT, self.project_dir, "template.py"), "r") as f:
            template = f.read()
        
        config = import_user_module("config")
        scraper_class = interprete(template, "name", syncb_command.settings)
        
        crawler_class = CrawlerCompiler(config, [scraper_class]).compile()
        crawler_class().start()
        
        
        
    
