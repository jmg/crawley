from eventlet import GreenPool
import elixir

import urllib2
import shutil
import os.path
from lxml import etree
from StringIO import StringIO

from crawley.crawlers import BaseCrawler 
from crawley.persistance import Entity, UrlEntity, session
from crawley.persistance import setup

from utils import import_user_module, inspect_module, generate_template, get_full_template_path

commands = {}


def command(store=commands):
    """
        Decorator that adds a command to a dictionary
    """
            
    def wrap(f):            

        store[f.__name__] = f
    
        def decorated(*args, **kwargs):
            f(*args, **kwargs)
    
        return decorated
    return wrap


@command
def startproject(*args):
    """
        Starts a new crawley project. 
        
        Copies the files inside conf/project_template in order 
        to generate a new project
    """
    
    if len(args) < 1:
        print "No given project name"
        sys.exit(1)
    
    project_name = args[0]
    
    if not os.path.exists(project_name):
        shutil.os.mkdir(project_name)        
                
    generate_template("settings", project_name, project_name)
    
    crawler_dir = os.path.join(project_name, project_name)
    if not os.path.exists(crawler_dir):
        shutil.os.mkdir(crawler_dir)
        
    generate_template("models", project_name, crawler_dir)
    generate_template("crawlers", project_name, crawler_dir)


@command
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
    

@command
def shell(*args):
        
    if len(args) < 1:
        print "No given url"
        sys.exit(1)
        
    try:
        import IPython
    except ImportError:
        print "Please install the ipython console"
        sys.exit(1)
        
    url = args[0]
    html = urllib2.urlopen(url).read()
    
    parser = etree.HTMLParser()
    html = etree.parse(StringIO(html), parser)
    
    shell = IPython.Shell.IPShellEmbed(argv=[], user_ns={ 'html' : html })
    shell()
        
        
@command
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
