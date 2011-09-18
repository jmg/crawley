import sys
import os
from commands import commands

def run_cmd(args):
    """
        Runs a crawley's command
    """
        
    if len(args) <= 1:
        print "Subcommand not specified"
        sys.exit(1)
        
    cmd_name = args[1]
    cmd_args = args[2:]
    
    cmd = commands.get(cmd_name)
        
    if cmd is None:
        print "[%s] Subcommand not valid" % (cmd_name)
        sys.exit(1)
        
    cmd(*cmd_args)
        

def verify_settings():
    """
        Try to import the settings.py file
        and check for errors and warnings in it 
    """
    try:
        sys.path.append(os.getcwd())
        import settings
    except:
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

