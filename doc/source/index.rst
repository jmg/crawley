.. crawley documentation master file, created by
   sphinx-quickstart on Wed Sep 14 10:05:07 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Crawley's Documentation
===================================

Crawley is a pythonic Scraping / Crawling Framework intended to make easy the way you extract data from web pages into structured storages such as databases.

Start a New Project
-----------------------------------
.. code-block:: bash
    
    crawley-admin.py startproject [project_name]

Example
-----------------------------------

.. code-block:: bash
    
    crawley-admin.py startproject Google
    
    
Then you have a crawley's project directory with 2 files like these

crawlers.py

.. code-block:: python

    from crawley.crawlers import BaseCrawler
    from crawley.scrapers import BaseScraper
    from models import *

    class GoogleScraper(BaseScraper):
        
        matching_urls = ["www.google.com"]
        
        def scrape(self, html):
                    
            data = html("#als").html()
            GoogleClass(Google_attribute=data)


    class GoogleCrawler(BaseCrawler):
        
        start_urls = ["http://www.google.com"]    
        scrapers = [GoogleScraper]
        max_depth = 1


models.py

.. code-block:: python

    from crawley.persistance import Entity, UrlEntity, Field, Unicode

    class GoogleUrls(UrlEntity):    
        pass
        
    class GoogleClass(Entity):
        
        Google_attribute = Field(Unicode(255))
    

.. toctree::
    :maxdepth: 1
        

Another one named settings.py in wich you can set up the project's configuration:

.. code-block:: python

    import os 

    #Don't change this if you don't have renamed the project
    PROJECT_NAME = "Google"
    PROJECT_ROOT = os.path.join(os.getcwd(), PROJECT_NAME)

    DATABASE_ENGINE = 'sqlite'     #TODO: test elixir with several DB engines
    DATABASE_NAME = 'Google'  
    DATABASE_USER = ''             # Not used with sqlite3.
    DATABASE_PASSWORD = ''         # Not used with sqlite3.
    DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
    DATABASE_PORT = ''     

    SHOW_DEBUG_INFO = True


And a manage.py file that allows you to run the crawler:

.. code-block:: bash
    
    python manage.py run

Indices and tables
==================

* :ref:`search`

