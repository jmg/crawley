import sys
from optparse import OptionParser

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup

from eventlet import GreenPool

def import_user_module(module):
    
    try:
        return __import__(module, locals(), globals(), [])
    except ImportError:
        print "%s.py file not found!" % module.__name__
        sys.exit(1)  

models = import_user_module("models")
crawler = import_user_module("crawler")

def inspect_module(module, klass, get_first=False):
        
    objects = []
    for k,v in module.__dict__.iteritems():
        try:
            if issubclass(v, klass) and v is not klass:
                if get_first:
                    return v
                objects.append(v)
        except:
            pass
    if get_first:
        return None
    return objects

def start():
            
    Spiders = inspect_module(crawler, BaseCrawler)
    Storages = inspect_module(models, Entity)
    UrlStorage = inspect_module(models, UrlEntity, get_first=True)
        
    setup(Storages)
    
    pool = GreenPool()    
    for Spider in Spiders:
        spider = Spider(storage=UrlStorage, session=session)
        pool.spawn_n(spider.start())    

def add_options():
    
    parser = OptionParser()
    parser.add_option("-r", "--run", help="run crawley and be happy!", nargs=0)
    (options, args) = parser.parse_args()
    if len(sys.argv) <= 1:
        print parser.print_help()
    elif options.run is not None:        
        start()

if __name__ == '__main__':
    add_options()    
