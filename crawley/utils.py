"""Utilities module"""

def url_matcher(url, pattern):
    """
        Returns True if the url matches the given pattern
    """
    
    WILDCARD = "%"
        
    if pattern.startswith(WILDCARD) and pattern.endswith(WILDCARD):
        return pattern[1:-1] in url
    elif pattern.endswith(WILDCARD):
        return pattern[:-1] == url[:len(pattern)-1]
    elif pattern.startswith(WILDCARD):        
        return pattern[1:] == url[-len(pattern)+1:]
    else:
        return pattern == url
