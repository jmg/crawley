import elixir
from elixir import Entity, Field, Unicode, UnicodeText

elixir.metadata.bind = "sqlite:///crawler_test.sqlite"
elixir.metadata.bind.echo = True

session = elixir.session

class UrlEntity(Entity):
    
    href = Field(Unicode(255))
    parent = Field(Unicode(255))

def setup():
    
    elixir.setup_all()
    elixir.create_all()
