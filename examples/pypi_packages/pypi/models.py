from crawley.persistance import Entity, UrlEntity, Field, Unicode

class Package(Entity):
    
    #add your table fields here
    updated = Field(Unicode(255))    
    package = Field(Unicode(255))
    description = Field(Unicode(255))
