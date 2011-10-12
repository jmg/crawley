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
        
        self.syncdb = SyncDbCommand(args=self.args, settings=self.settings)
        self.syncdb.checked_execute()        

        self.project_type.run(self)
