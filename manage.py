import sys
from optparse import OptionParser

from crawley.crawlers import BaseCrawler 
from crawley.persistance import UrlEntity, session
from crawley.persistance import setup


def import_user_module(module):
    
    try:
        return __import__(module, locals(), globals(), [])
    except:
        print "%s.py file not found!" % module.__name__
        sys.exit(1)  

models = import_user_module("models")
crawler = import_user_module("crawler")

def inspect_module(module, klass):
        
    for k,v in module.__dict__.iteritems():
        try:
            if issubclass(v, klass) and v is not klass:
                return v
        except:
            pass        

def start():
            
    Spider = inspect_module(crawler, BaseCrawler)
    Storage = inspect_module(models, UrlEntity)
    
    setup([Storage])
    
    spider = Spider(storage=Storage, session=session)
    spider.start()

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
