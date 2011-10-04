import elixir
from crawley.persistance import Entity, setup
from crawley.persistance.connectors import connectors

from command import ProjectCommand
from utils import inspect_module, import_user_module


class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"        
        
    def execute(self):
        
        if not hasattr(self.settings, "DATABASE_ENGINE") or not self.settings.DATABASE_ENGINE:
            return
        
        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)
        
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO
        
        models = import_user_module("models")
        Entities = inspect_module(models, Entity)
        setup(Entities)
        
