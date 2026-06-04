"""``run`` command: sync the database and run the user's crawlers."""

from crawley.manager.commands.command import ProjectCommand
from crawley.manager.commands.syncdb import SyncDbCommand


class RunCommand(ProjectCommand):
    """Read ``crawlers.py`` and run every user crawler."""

    name = "run"

    def execute(self):
        self.syncdb = SyncDbCommand(
            args=self.args, settings=self.settings, **self.kwargs
        )
        self.syncdb.checked_execute()

        self.project_type.run(self)
