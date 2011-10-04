import types
from crawley.scrapers import BaseScraper


class Interpreter(object):
    """
        This class "compiles" the DSL into scraper classes for
        the crawley framework
    """
    
    def __init__(self, sentences):
        
        self.sentences = sentences
                
    def compile(self):
        """
            Returns a runtime generated scraper class
        """
        
        attrs_dict = self._gen_method()
        return self._gen_class(attrs_dict)
    
    def _gen_class(self, attrs_dict):
        """
            Generates a scraper class
        """
        
        return type("GeneratedScraper", (BaseScraper, ), attrs_dict)
    
    def _gen_method(self):
        """
            Generates scrapers methods.
            Returns a dictionary containing methods and attributes for the
            scraper class.
        """
        
        def scrape(self, html):
            """
                Generated scrape method
            """
            
            for field, selector in self.sentences:
                
                node = html.xpath(selector)[0]
                field = _get_text_recursive(node)            
            
        def _get_text_recursive(node):
            """
                Extract the text from html nodes recursively.
            """
                
            if node.text is not None:
                return node.text
                
            childs = node.getchildren()
                    
            for child in childs:
                return _get_text_recursive(child)
                
        return { "scrape" : scrape, "sentences" : self.sentences }
