"""The crawley command line management interface."""

import sys

from crawley.manager.commands import commands
from crawley.utils import exit_with_error


def run_cmd(args):
    """Run a crawley command given the full ``argv`` list."""
    if len(args) <= 1:
        exit_with_error("Subcommand not specified")

    cmd_name = args[1]
    cmd_args = args[2:]

    cmd = commands[cmd_name](cmd_args)
    cmd.checked_execute()


def manage():
    """Entry point for the ``crawley`` console script."""
    run_cmd(sys.argv)
