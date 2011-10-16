Pypi Example
-----------------------------------

Lets make a scraper that extract data from the pypi's front page

http://pypi.python.org/pypi

Supose that we want extract data from the packages table and
store it in a database.

First at all we need to start a new crawley's project. In this case
it will be called pypi_packages.

.. code-block:: bash
    
    crawley startproject pypi_packages
    cd pypi_packages
    
Then, inside the pypi_packages there will a settings.py file and another 
directory containing a crawlers.py file and a models.py file.

Lets start defining the models.py wich is very simple in this case.

Models
===========

.. code-block:: python

    from crawley.persistance import Entity, UrlEntity, Field, Unicode

    class Package(Entity):
    
        #add your table fields here
        updated = Field(Unicode(255))    
        package = Field(Unicode(255))
        description = Field(Unicode(255))

As you can see, we just need a simple Package table that matches the data
we want to extract.

Ok, now is time to code. Lets make the scraper. It must be located inside
the crawlers.py file

Crawlers
===========

.. code-block:: python

    from crawley.crawlers import BaseCrawler
    from crawley.scrapers import BaseScraper
    from crawley.extractors import XPathExtractor
    from models import *

    class pypiScraper(BaseScraper):
        
        #specify the urls that can be scraped by this class
        matching_urls = ["%"]
        
        def scrape(self, response):
                            
            #getting the html table
            table = response.html.xpath("/html/body/div[5]/div/div/div[3]/table")[0]
            
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


The interesting part of this is the scrape method defined inside the 
pypiScraper class. It uses Xpath in order to obtain the parsed html 
and then stores the extracted data in the Packages table.

At this time we have finished our work. Very simple. Isn't it?

Run crawley
===========

Finally, just run the crawler (Ensure you are in the same directory where the
settings.py file is, in other case you can specify your settings directory
with --settings=path/to/your/settings.py)

.. code-block:: bash
    
    ~$ crawley run

And we are done. Check the results in your database!

Downloading the Code
====================

The entire code is located in the crawley's official repository at:

https://github.com/jmg/crawley/tree/master/examples/pypi_packages
