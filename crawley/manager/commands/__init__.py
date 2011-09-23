"""
    All Crawley's commands must be here
"""

from utils import exit_with_error

from run import RunCommand
from shell import ShellCommand
from startproject import StartProjectCommand
from syncdb import SyncDbCommand

class CommandsDict(dict):
    
    def __getitem__(self, key):
        
        if key in self:
            return dict.__getitem__(self, key)
        else:
            exit_with_error("[%s] Subcommand not valid" % (key))
            

commands = CommandsDict()

d = { RunCommand.name : RunCommand,
      ShellCommand.name : ShellCommand,
      StartProjectCommand.name : StartProjectCommand,
      SyncDbCommand.name : SyncDbCommand }

commands.update(d)

