import elixir
from elixir import Field, Unicode, UnicodeText

session = elixir.session

class Entity(elixir.EntityBase):                
    
    __metaclass__ = elixir.EntityMeta

class UrlEntity(elixir.EntityBase):
            
    href = Field(Unicode(255))
    parent = Field(Unicode(255))
    
    __metaclass__ = elixir.EntityMeta

def setup(entities):
    
    elixir.setup_entities(entities)
    elixir.create_all()

