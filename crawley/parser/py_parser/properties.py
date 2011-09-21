"""
    Properties
"""

class Property(object):
    
    @classmethod
    def populateProperties(self):
        
        propertyElements = {}
        propertyElements["id"] = IDProperty()
        propertyElements["tag"] = TagProperty()
        propertyElements["class"] = ClassProperty()
        return propertyElements
    
    @classmethod
    def getProperty(self, property):
        return self.populateProperties().get(property);
        

class ClassProperty(Property):
    
    def __str__(self):
        return "."

class IDProperty(Property):
    
    def __str__(self):
        return "#"

class TagProperty(Property):
    
    def __str__(self):
        return ""
