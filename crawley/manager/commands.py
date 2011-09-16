from eventlet import GreenPool
import elixir

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup

from utils import import_user_module, inspect_module, command

commands = {}


@command(commands)
def syncdb(settings):    
    """
        Build up the DataBase. 
        
        Reads the models.py user's file and generate a database from it.        
    """
    
    elixir.metadata.bind = "%s:///%s" % (settings.DATABASE_ENGINE, settings.DATABASE_NAME)
    elixir.metadata.bind.echo = settings.SHOW_DEBUG_INFO
    
    models = import_user_module("models")
    Entities = inspect_module(models, Entity)
    setup(Entities)
    

@command(commands)
def run(settings):
    """
        Run the user's crawler
        
        Reads the crawlers.py file to obtain the user's crawler classes
        and then run these crawlers.
    """
    
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
    
