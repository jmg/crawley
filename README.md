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
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class pypiScraper(BaseScraper):
    
    #specify the urls that can be scraped by this class
    matching_urls = ["%"]
    
    def scrape(self, html):
                        
        #getting the html table
        table = html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]
        
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

------------------------------------------------------------------

### Finally, just run the crawler

```bash
~$ crawley run
```


