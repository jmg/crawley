import sys
from commands import commands
from generators import generators

def run_cmd(settings, args):
    """
        Runs a crawley's command
    """
        
    if len(args) <= 1:
        print "Subcommand not specified"
        sys.exit(1)
        
    cmd_name = args[1]
    cmd_args = args[2:]
    
    if settings is not None:
        cmd = commands.get(cmd_name)
    else:
        cmd = generators.get(cmd_name)
        
    if cmd is None:
        print "[%s] Subcommand not valid" % (cmd_name)
        sys.exit(1)
    
    if settings is not None:
        cmd(settings, *cmd_args)
    else:
        cmd(*cmd_args)
        

def verify_settings(settings):
    """
        Check for errors and warnings in the settings.py file 
    """
    
    if settings.DATABASE_ENGINE == 'sqlite':
        if not settings.DATABASE_NAME.endswith(".sqlite"):
            settings.DATABASE_NAME = "%s.sqlite" % settings.DATABASE_NAME 
    return settings
    

def manage(settings):
    """
        Called when using the manage.py file
    """
    
    settings = verify_settings(settings)
    sys.path.append(settings.PROJECT_ROOT)    
    run_cmd(settings, sys.argv)


def execute():
    """
        Called when using the crawley-admin.py file
    """
    
    run_cmd(None, sys.argv)
