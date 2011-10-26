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
        
        
class ScraperCantParseError(Exception):
    """
        Raised when a scraper can't parse an html page
    """
    
    def __init__(self, *args, **kwargs):
        
        Exception.__init__(self, *args, **kwargs)


class InvalidProjectError(Exception):
    """
        Raised when the user opens a invalid directory with the browser
    """
    
    def __init__(self, *args, **kwargs):
        
        Exception.__init__(self, *args, **kwargs)
