import sys

from commands import commands
from crawley.utils import exit_with_error

def run_cmd(args):
    """
        Runs a crawley's command
    """
        
    if len(args) <= 1:
        exit_with_error("Subcommand not specified")
        
    cmd_name = args[1]
    cmd_args = args[2:]
    
    cmd = commands[cmd_name](cmd_args)    
    cmd.checked_execute()
        

def manage():
    """
        Called when using crawley command from cmd line
    """        
    run_cmd(sys.argv)

