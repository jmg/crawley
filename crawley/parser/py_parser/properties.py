"""
    Properties
"""

class Property(object):
    pass

class ClassProperty(Property):
    
    def __str__(self):
        return "."

class IDProperty(Property):
    
    def __str__(self):
        return "#"

class TagProperty(Property):
    
    def __str__(self):
        return ""
