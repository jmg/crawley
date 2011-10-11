import elixir
import os

from crawley.manager.utils import generate_template

from crawley.persistance import Entity, UrlEntity, setup
from crawley.persistance.connectors import connectors

from crawley.persistance.databases import session as database_session
from crawley.persistance.documents import json_session, JSONDocument
from crawley.persistance.documents import xml_session, XMLDocument
from crawley.persistance.documents import documents_entities

from base import BaseProject
from crawley.manager.utils import import_user_module, search_class


class CodeProject(BaseProject):
    
    name = "code"        
    
    def set_up(self, project_name):
        
        BaseProject.set_up(self, project_name)
        
        crawler_dir = os.path.join(project_name, project_name)
        self._create_module(crawler_dir)
                
        generate_template("models", project_name, crawler_dir)
        generate_template("crawlers", project_name, crawler_dir)
    
    def syncdb(self, syncb_command):
        
        syncb_command.sessions = []
                
        models = import_user_module("models")
                
        if search_class(JSONDocument, documents_entities) is not None:
            syncb_command.sessions.append(json_session)
            
        if search_class(XMLDocument, documents_entities) is not None:
            syncb_command.sessions.append(xml_session)
        
        if not hasattr(syncb_command.settings, "DATABASE_ENGINE") or not syncb_command.settings.DATABASE_ENGINE:                    
            return
        
        syncb_command.sessions.append(database_session)
        connector = connectors[syncb_command.settings.DATABASE_ENGINE](syncb_command.settings)
        
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = syncb_command.settings.SHOW_DEBUG_INFO
                
        setup(elixir.entities)
