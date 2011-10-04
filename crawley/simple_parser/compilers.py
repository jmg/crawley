import types
from crawley.scrapers import BaseScraper


class Interpreter(object):
    """
        This class "compiles" the DSL into scraper classes for
        the crawley framework
    """
    
    TEMPLATE_LINE = "def scrape(self, html): %s = html.xpath('%s')[0].text\n"
    
    def __init__(self, sentences):
        
        self.sentences = sentences
        
    def compile(self):
        
        method_lines = []
        for field, selector in self.sentences:
             method_lines.append(self._gen_line_method(field, selector))
            
        method = self._gen_method(method_lines)
        return self._gen_class(method)
    
    def _gen_class(self, functions_dict):
        
        klass = type("GeneratedScraper", (BaseScraper,), {"scrape" : functions_dict["scrape"]})
        return klass
    
    def _gen_method(self, code_lines):
            
        code = "".join(code_lines)
        code_object = compile(code, "", "exec")
        functions = {}
        exec code_object in functions
        return functions
    
    def _gen_line_method(self, field, selector):
        
        return self.TEMPLATE_LINE % (field, selector)
        
        
def test():
        
    i = Interpreter([("zarasa", "/html/body")])
    return i.compile()

from crawley.extractors import XPathExtractor
Scraper = test()
html = XPathExtractor().get_object(open("../../url.html").read())
Scraper().scrape(html)
