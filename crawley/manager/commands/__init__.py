"""
    All Crawley's commands must be here
"""

from utils import exit_with_error

from run import RunCommand
from shell import ShellCommand
from startproject import StartProjectCommand
from syncdb import SyncDbCommand

class CommandsDict(dict):
    
    def get(self, key):
        
        if key in self.keys():
            return self[key]
        else:
            exit_with_error("[%s] Subcommand not valid" % (key))
            

commands = CommandsDict()

commands.update({ RunCommand.name : RunCommand,
                  ShellCommand.name : ShellCommand,
                  StartProjectCommand.name : StartProjectCommand,
                  SyncDbCommand.name : SyncDbCommand})

