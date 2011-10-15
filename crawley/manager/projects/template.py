import os.path

from crawley.manager.utils import generate_template
from crawley.simple_parser import interprete
from crawley.simple_parser.compilers import CrawlerCompiler
from crawley.persistance import session

from base import BaseProject
from crawley.manager.utils import generate_template, import_user_module


class TemplateProject(BaseProject):
    
    name = "template"
    
    def set_up(self, project_name):
        
        BaseProject.set_up(self, project_name)
                
        generate_template("template", project_name, self.project_dir)
        generate_template("config", project_name, self.project_dir)
        
    def syncdb(self, syncb_command):
        
        with open(os.path.join(syncb_command.settings.PROJECT_ROOT, "template.crw"), "r") as f:
            template = f.read()                        
                                    
        syncb_command.scraper_class = interprete(template, syncb_command.settings)
        
    def run(self, run_command):
        
        config = import_user_module("config")                
        
        crawler_class = CrawlerCompiler(config, [run_command.syncdb.scraper_class]).compile()
        
        global session
        sessions = [session]
        crawler = crawler_class(sessions=sessions, debug=run_command.settings.SHOW_DEBUG_INFO)
        crawler.start()
        
        for session in sessions:
            session.close()
        
