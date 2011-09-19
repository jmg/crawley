from utils import exit_with_error

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
