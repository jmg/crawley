import elixir
from crawley.persistance import Entity, setup
from crawley.persistance.connectors import connectors

from crawley.persistance.databases import session as database_session
from crawley.persistance.documents import json_session, JSONDocument
from crawley.persistance.documents import xml_session, XMLDocument

from command import ProjectCommand
from utils import inspect_module, import_user_module


class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
        
        self.sessions = []
                
        models = import_user_module("models")
        
        if inspect_module(models, JSONDocument, get_first=True) is not None:
            self.sessions.append(json_session)
            
        if inspect_module(models, XMLDocument, get_first=True) is not None:
            self.sessions.append(xml_session)
        
        if not hasattr(self.settings, "DATABASE_ENGINE") or not self.settings.DATABASE_ENGINE:                    
            return
        
        self.sessions.append(database_session)
        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)
        
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO        
        
        Entities = inspect_module(models, Entity)
        setup(Entities)
