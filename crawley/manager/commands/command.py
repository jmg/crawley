import sys
import os 

from utils import exit_with_error, import_user_module

class BaseCommand(object):
    """
        Base Crawley's Command
    """
    
    name = "BaseCommand"
    requires_settings = False
    
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
        if self.requires_settings:
            self.settings = self._check_for_settings()
        self.execute()
        
    def _check_for_settings(self):
        """
            tries to import the user's settings file
        """
        
        if len(self.args) > 0 and "--settings=" in self.args[0]:
            settings_str = self.args[0].split("=")[1]
            settings_dir, file_name = settings_str.rsplit("/")
            sys.path.append(settings_dir)
            settings_file = file_name[:-3]
        else:
            sys.path.append(os.getcwd())
            settings_file = "settings"
        
        settings = import_user_module(settings_file)
            
        settings = self._check_setttings_errors(settings)
        sys.path.append(settings.PROJECT_ROOT)
        return settings
            
    def _check_setttings_errors(self, settings):
        
        if settings.DATABASE_ENGINE == 'sqlite':
            if not settings.DATABASE_NAME.endswith(".sqlite"):
                settings.DATABASE_NAME = "%s.sqlite" % settings.DATABASE_NAME 
            
        return settings
