import sys
import os 
from optparse import OptionParser

from utils import exit_with_error, import_user_module


class BaseCommand(object):
    """
        Base Crawley's Command
    """
    
    name = "BaseCommand"
    
    def __init__(self, args):
        
        self.args = args
        
    def check_validations(self):
        """
            Checks for validations
        """
        
        for validation, message in self.validations():
            if not validation:
                exit_with_error(message)
    
    def validations(self):
        """
            Returns a list of tuples containing:
                [(validate_condition, error_message)]
        """        
        
        return []
        
    def execute(self):
        """
            Executes the command
        """
        
        raise NotImplementedError()

    def checked_execute(self):
        """
            Checks before Execute
        """
        
        self.check_validations()
        self.execute()        
        

class ProjectCommand(BaseCommand):
    """
        A command that requires a settings.py file to run
    """
    
    def checked_execute(self):
        """
            Checks for settings before run
        """
        
        self._add_options()
        self.settings = self._check_for_settings()
        BaseCommand.checked_execute(self)
        
    def _add_options(self):
        """
            Add options that can be procesed by OptionParser
        """
        
        self.parser = OptionParser()
        self.parser.add_option("-s", "--settings", help="Indicates the settings.py file")                                
    
    def _check_for_settings(self):
        """
            tries to import the user's settings file
        """
        
        (options, args) = self.parser.parse_args(self.args)
        
        if options.settings is not None:

            settings_dir, file_name = os.path.split(options.settings)
            
            sys.path.append(settings_dir)
            settings_file = os.path.splitext(file_name)[0]
            
        else:
            sys.path.append(os.getcwd())
            settings_file = "settings"
        
        settings = import_user_module(settings_file)
            
        settings = self._check_setttings_errors(settings)
        sys.path.append(settings.PROJECT_ROOT)
        return settings
            
    def _check_setttings_errors(self, settings):
        """
            Fix errors in settings.py
        """
        
        if settings.DATABASE_ENGINE == 'sqlite':
            if not settings.DATABASE_NAME.endswith(".sqlite"):
                settings.DATABASE_NAME = "%s.sqlite" % settings.DATABASE_NAME 
            
        return settings
