import elixir
from elixir import Field, Unicode, UnicodeText

session = elixir.session


class Entity(elixir.EntityBase):
    """
        Base Entity
        
        Every Crawley's Entity must Inherit from this class
    """
    
    __metaclass__ = elixir.EntityMeta


class UrlEntity(Entity):
    """
        Entity intended to save urls
    """
            
    href = Field(Unicode(255))
    parent = Field(Unicode(255))
    
    __metaclass__ = elixir.EntityMeta
    

def setup(entities):
    """
        Setup the database based on a list of user's entities
    """
    
    elixir.setup_entities(entities)
    elixir.create_all()

