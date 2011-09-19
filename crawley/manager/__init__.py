import sys
import os

from commands import commands
from commands.utils import exit_with_error

def run_cmd(args):
    """
        Runs a crawley's command
    """
        
    if len(args) <= 1:
        exit_with_error("Subcommand not specified")
        
    cmd_name = args[1]
    cmd_args = args[2:]
    
    cmd = commands.get(cmd_name)        
    
    command = cmd(cmd_args)    
    command.checked_execute()
        

def verify_settings():
    """
        Try to import the settings.py file
        and check for errors and warnings in it 
    """
    try:
        sys.path.append(os.getcwd())
        import settings
    except ImportError:
        return []
    
    if settings.DATABASE_ENGINE == 'sqlite':
        if not settings.DATABASE_NAME.endswith(".sqlite"):
            settings.DATABASE_NAME = "%s.sqlite" % settings.DATABASE_NAME 
            
    sys.path.append(settings.PROJECT_ROOT)
    
    return [settings]
    

def manage():
    """
        Called when using crawley command from cmd line
    """
    args = sys.argv
    args.extend(verify_settings())
    run_cmd(args)

