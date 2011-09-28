
class AuthenticationError(Exception):
    """
        Raised when a login error occurs
    """
    
    def __init__(self, *args, **kwargs):
        
        Exception.__init__(self, *args, **kwargs)
