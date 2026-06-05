"""All crawley management commands live here."""

from crawley.manager.commands.browser import BrowserCommand
from crawley.manager.commands.migratedb import MigrateDbCommand
from crawley.manager.commands.run import RunCommand
from crawley.manager.commands.shell import ShellCommand
from crawley.manager.commands.startproject import StartProjectCommand
from crawley.manager.commands.syncdb import SyncDbCommand
from crawley.utils.collections import CustomDict

commands = CustomDict(error="[%s] is not a valid subcommand")
commands.update(
    {
        RunCommand.name: RunCommand,
        ShellCommand.name: ShellCommand,
        StartProjectCommand.name: StartProjectCommand,
        SyncDbCommand.name: SyncDbCommand,
        BrowserCommand.name: BrowserCommand,
        MigrateDbCommand.name: MigrateDbCommand,
    }
)

__all__ = [
    "commands",
    "RunCommand",
    "ShellCommand",
    "StartProjectCommand",
    "SyncDbCommand",
    "BrowserCommand",
    "MigrateDbCommand",
]
