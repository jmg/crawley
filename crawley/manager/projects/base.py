import os.path
import shutil


import elixir
import crawley

from multiprocessing import Process

from crawley.manager.utils import generate_template, get_full_template_path, has_valid_attr
from crawley.persistance import Entity, UrlEntity, setup
from crawley.persistance.databases import session as database_session
from crawley.persistance.documents import json_session, JSONDocument, documents_entities, xml_session, XMLDocument
from crawley.persistance.connectors import connectors

class BaseProject(object):
    """
        Base of all crawley's projects
    """

    def set_up(self, project_name):
        """
            Setups a crawley project
        """

        self._create_module(project_name)
        self._write_meta_data(project_name)
        generate_template("settings", project_name, project_name)

        self.project_dir = os.path.join(project_name, project_name)
        self._create_module(self.project_dir)

    def _write_meta_data(self, directory_module):

        with open(get_full_template_path("metadata")) as f:
            data = f.read()

        data = data % { 'version' : crawley.__version__, 'type' : self.name }

        with open(os.path.join(directory_module, "__init__.py"), "w") as f:
            f.write(data)

    def _create_module(self, name):
        """
            Generates a python module with the given name
        """

        if not os.path.exists(name):

            shutil.os.mkdir(name)
            f = open(os.path.join(name, "__init__.py"), "w")
            f.close()

    def syncdb(self, syncb_command):
        """
            Checks for storages configuration in the settings.py file
        """

        self.connector = None
        syncb_command.sessions = []

        if has_valid_attr(syncb_command.settings, 'JSON_DOCUMENT'):

            json_session.file_name = syncb_command.settings.JSON_DOCUMENT
            syncb_command.sessions.append(json_session)

        if has_valid_attr(syncb_command.settings, 'XML_DOCUMENT'):

            xml_session.file_name = syncb_command.settings.XML_DOCUMENT
            syncb_command.sessions.append(xml_session)

        if has_valid_attr(syncb_command.settings, "DATABASE_ENGINE"):

            syncb_command.sessions.append(database_session)
            self.connector = connectors[syncb_command.settings.DATABASE_ENGINE](syncb_command.settings)

    def _setup_entities(self, entities, settings):

        elixir.metadata.bind = self.connector.get_connection_string()
        elixir.metadata.bind.echo = settings.SHOW_DEBUG_INFO

        setup(elixir.entities)

    def run(self, run_command, crawlers):

        for crawler_class in crawlers:

            crawler = crawler_class(sessions=run_command.syncdb.sessions, settings=run_command.settings)
            process = Process(target=crawler.start)
            process.start()
            process.join()

        for session in run_command.syncdb.sessions:
            session.close()

