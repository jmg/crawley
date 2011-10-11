import elixir
from crawley.persistance import Entity, UrlEntity, setup
from crawley.persistance.connectors import connectors

from crawley.persistance.databases import session as database_session
from crawley.persistance.documents import json_session, JSONDocument
from crawley.persistance.documents import xml_session, XMLDocument
from crawley.persistance.documents import documents_entities

from command import ProjectCommand
from utils import import_user_module, search_class


class SyncDbCommand(ProjectCommand):
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    name = "syncdb"
        
    def execute(self):
        
        self.sessions = []
                
        models = import_user_module("models")
                
        if search_class(JSONDocument, documents_entities):
            self.sessions.append(json_session)
            
        if search_class(XMLDocument, documents_entities):
            self.sessions.append(xml_session)
        
        if not hasattr(self.settings, "DATABASE_ENGINE") or not self.settings.DATABASE_ENGINE:                    
            return
        
        self.sessions.append(database_session)
        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)
        
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO
                
        setup(elixir.entities)
