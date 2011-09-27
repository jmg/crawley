import elixir
from crawley.persistance import Entity, setup

from command import ProjectCommand
from utils import inspect_module, import_user_module


class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
                
        elixir.metadata.bind = "%s:///%s" % (self.settings.DATABASE_ENGINE, self.settings.DATABASE_NAME)
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO
        
        models = import_user_module("models")
        Entities = inspect_module(models, Entity)        
        setup(Entities)
        
