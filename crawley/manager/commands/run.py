from eventlet import GreenPool

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, setup

from command import ProjectCommand
from syncdb import SyncDbCommand
from utils import inspect_module, import_user_module


class RunCommand(ProjectCommand):
    """
        Run the user's crawler
        
        Reads the crawlers.py file to obtain the user's crawler classes
        and then run these crawlers.
    """
    
    name = "run"
    
    def execute(self):                
                
        syncdb = SyncDbCommand(self.args)
        syncdb.checked_execute()
        
        crawler = import_user_module("crawlers")
        models = import_user_module("models")
        
        Spiders = inspect_module(crawler, BaseCrawler)    
        UrlStorage = inspect_module(models, UrlEntity, identity=True, get_first=True)
                    
        pool = GreenPool()    
        for Spider in Spiders:
        
            spider = Spider(storage=UrlStorage, debug=self.settings.SHOW_DEBUG_INFO)
            pool.spawn_n(spider.start)
            
        pool.waitall() 
