import types
from crawley.scrapers import BaseScraper
from crawley.crawlers import BaseCrawler
from crawley.persistance.databases import Entity, Field, Unicode, setup, session, elixir
from crawley.persistance.connectors import SqliteConnector


class Interpreter(object):
    """
        This class "compiles" the DSL into scraper classes for
        the crawley framework
    """
    
    def __init__(self, sentences, table_name, settings):
        
        self.sentences = sentences
        self.table_name = table_name
        self.settings = settings
                
    def compile(self):
        """
            Returns a runtime generated scraper class
        """
        self._gen_entities()                        
        
        attrs_dict = self._gen_scrape_method()
        return self._gen_scraper_class(attrs_dict)
    
    def _gen_scraper_class(self, attrs_dict):
        """
            Generates a scraper class
        """
        
        return type("GeneratedScraper", (BaseScraper, ), attrs_dict)
        
    def _gen_entities(self):
        """
            Generates an entity class
        """                
        
        self.fields = [s[0] for s in self.sentences]
        attrs_dict = dict([(field, Field(Unicode(255))) for field in self.fields])
        
        self.entity = type(self.table_name, (Entity, ), attrs_dict)
                
        connector = SqliteConnector(self.settings)
        
        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO
                
        setup([self.entity])
    
    def _gen_scrape_method(self):
        """
            Generates scrapers methods.
            Returns a dictionary containing methods and attributes for the
            scraper class.
        """
        sentences = self.sentences
        entity = self.entity
        
        def scrape(self, html):
            """
                Generated scrape method
            """            
            
            fields = {}
            
            for field, selector in sentences:
                
                nodes = html.xpath(selector)
                if nodes:
                    fields[field] = _get_text_recursive(nodes[0])
                        
            entity(**fields)
            session.commit()
            
            
        def _get_text_recursive(node):
            """
                Extract the text from html nodes recursively.
            """            
            if node.text is not None and node.text.strip():
                return node.text
                
            childs = node.getchildren()
                    
            for child in childs:
                return _get_text_recursive(child)            
                                        
        return { "scrape" : scrape, "matching_urls" : "%" }



class CrawlerCompiler(object):
    
    def __init__(self, config, scrapers):
        
        self.scrapers = scrapers
        self.config = config
        
    def compile(self):
        
        attrs_dict = {}
        attrs_dict["scrapers"] = []
        
        for scraper in self.scrapers:
            attrs_dict["scrapers"].append(scraper)
            
        attrs_dict["max_depth"] = self.config.max_depth
        attrs_dict["start_urls"] = self.config.start_urls
        
        return type("GeneratedCrawler", (BaseCrawler, ), attrs_dict)            
