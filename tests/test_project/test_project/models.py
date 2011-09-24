from crawley.persistance import Entity, UrlEntity, Field, Unicode

class test_projectUrls(UrlEntity):    
    pass
    
class test_projectClass(Entity):
    
    test_project_attribute = Field(Unicode(255))
