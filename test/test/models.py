from crawley.persistance import Entity, UrlEntity, Field, Unicode

class testUrls(UrlEntity):    
    pass
    
class testClass(Entity):
    
    test_attribute = Field(Unicode(255))
