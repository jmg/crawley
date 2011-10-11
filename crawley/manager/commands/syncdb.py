from crawley.manager.projects import CodeProject, TemplateProject
from crawley.manager.utils import import_user_module
from command import ProjectCommand

class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
        
        if import_user_module("template", exit=False) is not None:
            
            project = TemplateProject()
            
        elif import_user_module("models", exit=False) is not None:
            
            project = CodeProject()
        
        project.syncdb(self)
        
