"""
    Crawley exceptions
"""

class AuthenticationError(Exception):
    """
        Raised when a login error occurs
    """
    
    def __init__(self, *args, **kwargs):
        
        Exception.__init__(self, *args, **kwargs)


class TemplateSyntaxError(Exception):
    """
        DSL Template sintax error
    """
        
    def __init__(self, line=0, *args, **kwargs):
    
        self.line = line
        Exception.__init__(self, *args, **kwargs)
        
