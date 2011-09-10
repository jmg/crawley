import elixir
from elixir import Field, Unicode, UnicodeText

elixir.metadata.bind = "sqlite:///crawler_test.sqlite"
elixir.metadata.bind.echo = True

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

