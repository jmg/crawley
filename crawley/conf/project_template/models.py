from crawley.persistance import Entity, UrlEntity, Field, Unicode

class %(project_name)sUrls(UrlEntity):    
    pass
    
class %(project_name)sClass(Entity):
    
    %(project_name)s_attribute = Field(Unicode(255))
