from crawley.persistance import Entity, UrlEntity, Field, Unicode

class zarasaUrls(UrlEntity):    
    pass
    
class zarasaClass(Entity):
    
    zarasa_attribute = Field(Unicode(255))
