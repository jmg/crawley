# Pythonic Crawling / Scraping Framework Built on Eventlet 

------------------------------------------------------------------

### Features

* High Speed WebCrawler built on Eventlet.
* Supports databases engines like Postgre, Mysql, Oracle, Sqlite.
* Command line tools.
* Extract data using your favourite tool. XPath or Pyquery (A Jquery-like library for python).
* Cookie Handlers.
* Very easy to use (see the example).

### Documentation

http://packages.python.org/crawley/

------------------------------------------------------------------

### To install crawley run

```bash
~$ python setup.py install
```

### or from pip

```bash
~$ pip install crawley
```

------------------------------------------------------------------

### To start a new project run

```bash
~$ crawley startproject [project_name]
~$ cd [project_name]
```

------------------------------------------------------------------

### Write your Models

```python
""" models.py """

from crawley.persistance import Entity, UrlEntity, Field, Unicode

class Package(Entity):
    
    #add your table fields here
    updated = Field(Unicode(255))    
    package = Field(Unicode(255))
    description = Field(Unicode(255))
```

------------------------------------------------------------------

### Write your Scrapers

```python
""" crawlers.py """

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class pypiScraper(BaseScraper):
    
    #specify the urls that can be scraped by this class
    matching_urls = ["%"]
    
    def scrape(self, reponse):
                        
        #getting the current document's url.
        current_url = reponse.url        
        #getting the html table.
        table = reponse.html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]
        
        #for rows 1 to n-1
        for tr in table[1:-1]:
                        
            #obtaining the searched html inside the rows
            td_updated = tr[0]
            td_package = tr[1]
            package_link = td_package[0]
            td_description = tr[2]
            
            #storing data in Packages table
            Package(updated=td_updated.text, package=package_link.text, description=td_description.text)


class pypiCrawler(BaseCrawler):
    
    #add your starting urls here
    start_urls = ["http://pypi.python.org/pypi"]
    
    #add your scraper classes here    
    scrapers = [pypiScraper]
    
    #specify you maximum crawling depth level    
    max_depth = 0
    
    #select your favourite HTML parsing tool
    extractor = XPathExtractor
```

### Configure your settings

```python
""" settings.py """

import os 
PATH = os.path.dirname(os.path.abspath(__file__))

#Don't change this if you don't have renamed the project
PROJECT_NAME = "pypi"
PROJECT_ROOT = os.path.join(PATH, PROJECT_NAME)

DATABASE_ENGINE = 'sqlite'     
DATABASE_NAME = 'pypi'  
DATABASE_USER = ''             
DATABASE_PASSWORD = ''         
DATABASE_HOST = ''             
DATABASE_PORT = ''     

SHOW_DEBUG_INFO = True
```

------------------------------------------------------------------

### Finally, just run the crawler

```bash
~$ crawley run
```


