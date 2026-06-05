"""``syncdb`` command: build the database from the user's models."""

from crawley.manager.commands.command import ProjectCommand


class SyncDbCommand(ProjectCommand):
    """Read the ``models.py`` file and create the database from it."""

    name = "syncdb"

    def execute(self):
        self.project_type.syncdb(self)
