from eventlet import GreenPool
import elixir

import shutil
import os.path

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup
from crawley.extractors import XPathExtractor, PyQueryExtractor

from utils import *

commands = {}


def command(store):
    """
        Decorator that adds a command to a dictionary
    """
            
    def wrap(f):            

        store[f.__name__] = f
    
        def decorated(*args, **kwargs):
            f(*args, **kwargs)
    
        return decorated
    return wrap


@command(commands)
def startproject(*args):
    """
        Starts a new crawley project. 
        
        Copies the files inside conf/project_template in order 
        to generate a new project
    """
    
    if len(args) < 1:
        exit_with_error("No given project name")
    
    project_name = args[0]
    
    if not os.path.exists(project_name):
        shutil.os.mkdir(project_name)        
                
    generate_template("settings", project_name, project_name)
    
    crawler_dir = os.path.join(project_name, project_name)
    if not os.path.exists(crawler_dir):
        shutil.os.mkdir(crawler_dir)
        
    generate_template("models", project_name, crawler_dir)
    generate_template("crawlers", project_name, crawler_dir)


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
def shell(*args):
        
    if len(args) < 1:
        exit_with_error("No given url")
        
    try:
        import IPython
    except ImportError:
        exit_with_error("Please install the ipython console")
    
    url = args[0]
    crawler = BaseCrawler()
    
    data = crawler._get_data(url)
    html = XPathExtractor().get_object(data)
    
    shell = IPython.Shell.IPShellEmbed(argv=[], user_ns={ 'html' : html })
    shell()
        
        
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
    
        spider = Spider(storage=UrlStorage)
        pool.spawn_n(spider.start)
        
    pool.waitall() 
