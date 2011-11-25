from crawley.persistance import Entity, UrlEntity, Field, Unicode

class ebayUrls(UrlEntity):    
    
    #this entity is intended for save urls
    pass

class ebayClass(Entity):
    
    #add your table fields here
    title = Field(Unicode(2056))
    
    def __init__(self, title):
        self.title = title;
