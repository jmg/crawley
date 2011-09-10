from crawley.persistance import Entity, UrlEntity, Field, Unicode

class GoogleUrls(UrlEntity):    
    pass
    
class GoogleText(Entity):
    
    text = Field(Unicode(255))
    
    
