import os
import elixir
from eventlet import GreenPool

from crawley.persistance import Entity, UrlEntity, setup
from crawley.persistance.connectors import connectors

from crawley.persistance.databases import session as database_session
from crawley.persistance.documents import json_session, JSONDocument, documents_entities, xml_session, XMLDocument
from crawley.persistance import UrlEntity

from crawley.manager.utils import import_user_module, search_class, generate_template
from crawley.crawlers import user_crawlers

from base import BaseProject


class CodeProject(BaseProject):
    """
        This class represents a code project.
        It can be started with:
        
            ~$ crawley startproject -t code [name]
    """
    
    name = "code"        
    
    def set_up(self, project_name):
        """
            Setups a code project.
            Generates the crawlers and models files based on a template.
        """
        
        BaseProject.set_up(self, project_name)                
                
        generate_template("models", project_name, self.project_dir)
        generate_template("crawlers", project_name, self.project_dir)
    
    def syncdb(self, syncb_command):
        """
            Builds the database and find the documents storages.
            Foreach storage it adds a session to commit the results.
        """
        
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
    
    def run(self, run_command):
        """
            Run the crawler of a code project
        """
        
        crawler = import_user_module("crawlers")
        models = import_user_module("models")
                
        url_storage = search_class(UrlEntity, elixir.entities)
        
        pool = GreenPool()                
                
        for crawler_class in user_crawlers:

            spider = crawler_class(storage=url_storage, sessions=run_command.syncdb.sessions, debug=run_command.settings.SHOW_DEBUG_INFO)
            pool.spawn_n(spider.start)

        pool.waitall()
        for session in run_command.syncdb.sessions:
            session.close()
        
