"""Base project type shared by code and template projects."""

import asyncio
import os.path

import crawley
from crawley.persistance.documents import (
    csv_session,
    json_session,
    xml_session,
)
from crawley.persistance.nosql.couch import couch_session
from crawley.persistance.nosql.mongo import mongo_session
from crawley.persistance.relational.connectors import connectors
from crawley.persistance.relational.databases import session as database_session
from crawley.persistance.relational.databases import setup
from crawley.utils import (
    generate_template,
    get_full_template_path,
    has_valid_attr,
    import_user_module,
)


class BaseProject:
    """Base of all crawley projects."""

    name = "base"

    def set_up(self, project_name, base_dir=None):
        """Set up a crawley project skeleton."""
        main_module = project_name
        if base_dir is not None:
            main_module = os.path.join(base_dir, project_name)

        self._create_module(main_module)
        self._write_meta_data(main_module)

        generate_template("settings", project_name, main_module)

        self.project_dir = os.path.join(main_module, project_name)
        self._create_module(self.project_dir)

    def _write_meta_data(self, directory_module):
        with open(get_full_template_path("metadata")) as f:
            data = f.read()

        data = data % {"version": crawley.__version__, "type": self.name}

        with open(os.path.join(directory_module, "__init__.py"), "w") as f:
            f.write(data)

    def _create_module(self, name):
        if not os.path.exists(name):
            os.mkdir(name)
            open(os.path.join(name, "__init__.py"), "w").close()

    def syncdb(self, syncb_command):
        """Configure the storages declared in ``settings.py``."""
        self.connector = None
        syncb_command.sessions = []

        documents_sessions = {
            "JSON_DOCUMENT": json_session,
            "XML_DOCUMENT": xml_session,
            "CSV_DOCUMENT": csv_session,
            "MONGO_DB_HOST": mongo_session,
            "COUCH_DB_HOST": couch_session,
        }

        for storage_name, session in documents_sessions.items():
            if has_valid_attr(syncb_command.settings, storage_name):
                session.set_up(syncb_command.settings, storage_name)
                syncb_command.sessions.append(session)

        if has_valid_attr(syncb_command.settings, "DATABASE_ENGINE"):
            import_user_module("models", exit=False)
            syncb_command.sessions.append(database_session)
            self.connector = connectors[syncb_command.settings.DATABASE_ENGINE](
                syncb_command.settings
            )

    def _setup_entities(self, settings):
        setup(
            self.connector.get_connection_string(),
            echo=getattr(settings, "SHOW_DEBUG_INFO", False),
        )

    def run(self, run_command, crawlers):
        """Instantiate and run every crawler concurrently."""
        instances = [
            crawler_class(
                sessions=run_command.syncdb.sessions, settings=run_command.settings
            )
            for crawler_class in crawlers
        ]

        async def _run_all():
            await asyncio.gather(*(crawler.start() for crawler in instances))

        asyncio.run(_run_all())

        for session in run_command.syncdb.sessions:
            session.close()
