from command import ProjectCommand
from crawley.utils import import_user_module
from crawley.persistance.relational.connectors import connectors
from syncdb import SyncDbCommand
import elixir

class MigrateDbCommand(ProjectCommand):
    """
        Migrate up the DataBase.

        Reads the models.py user's file and generate a database from it.
    """

    name = "migratedb"

    def execute(self):
        self.syncdb = SyncDbCommand(args=self.args, settings=self.settings, **self.kwargs)

        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO
        elixir.cleanup_all(True)

        self.syncdb.checked_execute()
