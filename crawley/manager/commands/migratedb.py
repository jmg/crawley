"""``migratedb`` command: drop and recreate the database tables."""

from crawley.manager.commands.command import ProjectCommand
from crawley.manager.commands.syncdb import SyncDbCommand
from crawley.persistance.relational.connectors import connectors
from crawley.persistance.relational.databases import Base, setup
from crawley.utils import import_user_module


class MigrateDbCommand(ProjectCommand):
    """Recreate the database from the user's models, dropping existing tables."""

    name = "migratedb"

    def execute(self):
        import_user_module("models", exit=False)

        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)
        engine = setup(
            connector.get_connection_string(),
            echo=getattr(self.settings, "SHOW_DEBUG_INFO", False),
        )
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        self.syncdb = SyncDbCommand(
            args=self.args, settings=self.settings, **self.kwargs
        )
        self.syncdb.checked_execute()
