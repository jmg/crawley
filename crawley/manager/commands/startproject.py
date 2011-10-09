import shutil
import os.path

from command import BaseCommand
from utils import generate_template


class StartProjectCommand(BaseCommand):
    """
        Starts a new crawley project. 
        
        Copies the files inside conf/project_template in order 
        to generate a new project
    """
    
    name = "startproject"
    
    def validations(self):
                
        return [(len(self.args) >= 1, "No given project name")]

    def execute(self):
                        
        project_name = self.args[0]
        
        self._create_module(project_name)                    
        generate_template("settings", project_name, project_name)
        
        crawler_dir = os.path.join(project_name, project_name)
        self._create_module(crawler_dir)
                
        generate_template("models", project_name, crawler_dir)
        generate_template("crawlers", project_name, crawler_dir)

    def _create_module(self, name):
        
        if not os.path.exists(name):            
            shutil.os.mkdir(name)
            f = open(os.path.join(name, "__init__.py"), "w")            
            f.close()
