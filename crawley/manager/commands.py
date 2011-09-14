from eventlet import GreenPool
import elixir

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup

from utils import import_user_module, inspect_module


commands = {}

def command(f):
    
    commands[f.__name__] = f
    
    def decorated(*args, **kwargs):
        f(*args, **kwargs)
    
    return decorated


@command 
def syncdb(settings):
    
    elixir.metadata.bind = "%s:///%s" % (settings.DATABASE_ENGINE, settings.DATABASE_NAME)
    elixir.metadata.bind.echo = settings.SHOW_DEBUG_INFO
    
    models = import_user_module("models")
    Entities = inspect_module(models, Entity)
    setup(Entities)
    

@command
def run(settings):
    
    syncdb(settings)
    crawler = import_user_module("crawlers")
    models = import_user_module("models")
    
    Spiders = inspect_module(crawler, BaseCrawler)    
    UrlStorage = inspect_module(models, UrlEntity, get_first=True)
                
    pool = GreenPool()    
    for Spider in Spiders:
    
        spider = Spider(storage=UrlStorage, session=session)        
        pool.spawn_n(spider.start)
        
    pool.waitall()    
    
