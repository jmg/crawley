import sys
from commands import commands

def run_cmd(settings, args):
        
    if len(args) <= 1:
        print "Subcommand not specified"
    else:
        cmd_name = args[1]
        cmd_args = args[2:]
        cmd = commands.get(cmd_name)
        if cmd is None:
            print "[%s] Subcommand not valid" % (cmd_name)
        else:
            cmd(settings, *cmd_args)


def verify_settings(settings):
    
    if settings.DATABASE_ENGINE == 'sqlite':
        if not settings.DATABASE_NAME.endswith(".sqlite"):
            settings.DATABASE_NAME = "%s.sqlite" % settings.DATABASE_NAME 
    return settings
    

def manage(settings):
    
    settings = verify_settings(settings)
    sys.path.append(settings.PROJECT_ROOT)
    run_cmd(settings, sys.argv)
