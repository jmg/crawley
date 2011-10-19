import os.path
import shutil

from crawley.manager.utils import generate_template

class BaseProject(object):
    """
        Base of all crawley's projects
    """
    
    def set_up(self, project_name):
        """
            Setups a crawley project
        """
        
        self._create_module(project_name)                    
        generate_template("settings", project_name, project_name)
        
        self.project_dir = os.path.join(project_name, project_name)
        self._create_module(self.project_dir)
    
    def _create_module(self, name):
        """
            Generates a python module with the given name
        """
        
        if not os.path.exists(name):
            
            shutil.os.mkdir(name)
            f = open(os.path.join(name, "__init__.py"), "w")            
            f.close()
            
