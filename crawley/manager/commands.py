from eventlet import GreenPool
import elixir

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup

from utils import import_user_module, inspect_module


commands = {}

def command(f):
    
    commands[f.__name__] = f


@command
def run(settings):
    
    elixir.metadata.bind = "%s:///%s" % (settings.DATABASE_ENGINE, settings.DATABASE_NAME)
    elixir.metadata.bind.echo = True
    
    models = import_user_module("models")
    crawler = import_user_module("crawler")
            
    Spiders = inspect_module(crawler, BaseCrawler)    
    Entities = inspect_module(models, Entity)    
    UrlStorage = inspect_module(models, UrlEntity, get_first=True)
        
    setup(Entities)
    
    pool = GreenPool()    
    for Spider in Spiders:
    
        spider = Spider(storage=UrlStorage, session=session)        
        pool.spawn_n(spider.start)
        
    pool.waitall()    



