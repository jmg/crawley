import os.path
import shutil

from crawley.manager.utils import generate_template


class BaseProject(object):
    
    def set_up(self, project_name):
        
        self._create_module(project_name)                    
        generate_template("settings", project_name, project_name)
    
    def _create_module(self, name):
        
        if not os.path.exists(name):
            
            shutil.os.mkdir(name)
            f = open(os.path.join(name, "__init__.py"), "w")            
            f.close()
            
