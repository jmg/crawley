"""
    All Crawley's commands must be here
"""

from run import RunCommand
from shell import ShellCommand
from startproject import StartProjectCommand
from syncdb import SyncDbCommand

commands = { RunCommand.name : RunCommand,
             ShellCommand.name : ShellCommand,
             StartProjectCommand.name : StartProjectCommand,
             SyncDbCommand.name : SyncDbCommand, }

