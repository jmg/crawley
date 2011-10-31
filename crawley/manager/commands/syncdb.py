from crawley.utils import import_user_module
from command import ProjectCommand

class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
                        
        self.project_type.syncdb(self)
        
