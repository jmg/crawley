import elixir
from crawley.persistance import Entity, setup

from command import BaseCommand
from ..utils import inspect_module, import_user_module


class SyncDbCommand(BaseCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
        
        settings = self.args[0]
        
        elixir.metadata.bind = "%s:///%s" % (settings.DATABASE_ENGINE, settings.DATABASE_NAME)
        elixir.metadata.bind.echo = settings.SHOW_DEBUG_INFO
        
        models = import_user_module("models")
        Entities = inspect_module(models, Entity)
        setup(Entities)
        
