"""
    Properties
"""
from utils import UncasedDict

class Property(UncasedDict):
    
    def __init__(self):
        dict.__init__(self)
        self["id"] = IDProperty().__str__()
        self["tag"] = TagProperty().__str__()
        self["class"] = ClassProperty().__str__()
    
class ClassProperty(object):
    
    def __str__(self):
        return "."

class IDProperty(object):
    
    def __str__(self):
        return "#"

class TagProperty(object):
    
    def __str__(self):
        return ""
