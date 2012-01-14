from crawley.persistance import Entity, UrlEntity, Field, Unicode

class PackagesUrls(UrlEntity):

    #this entity is intended for save urls
    pass

class PackagesAuthors(Entity):

    #add your table fields here
    project = Field(Unicode(255))
    author = Field(Unicode(255))

