from crawley.persistance import MongoEntity, Field, Unicode

class Package(MongoEntity):

    #add your table fields here
    updated = Field(Unicode(255))
    package = Field(Unicode(255))
    description = Field(Unicode(255))
