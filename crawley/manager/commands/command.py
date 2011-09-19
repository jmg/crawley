
class BaseCommand(object):
    """
        Base Crawley's Command
    """
    
    name = "BaseCommand"
    
    def __init__(self, *args):
        
        self.args = args
    
    def validate(self):
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
