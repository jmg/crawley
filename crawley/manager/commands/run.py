from command import ProjectCommand
from syncdb import SyncDbCommand


class RunCommand(ProjectCommand):
    """
        Run the user's crawler

        Reads the crawlers.py file to obtain the user's crawler classes
        and then run these crawlers.
    """

    name = "run"

    def execute(self):
        
        if "syncdb" not in self.kwargs or not self.kwargs["syncdb"]:
            self.syncdb = SyncDbCommand(args=self.args, settings=self.settings, **self.kwargs)
            self.syncdb.checked_execute()
        else :
            self.syncdb = self.kwargs["syncdb"]

        self.project_type.run(self)
