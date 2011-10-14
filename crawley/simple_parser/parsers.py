from crawley.exceptions import TemplateSyntaxError

class DSLAnalizer(object):
    """
        Analizes the DSL written by users
    """
    
    def __init__(self, dsl):
        
        self.dsl = dsl
    
    def parse(self):
        
        dsl_scrapers = []
        
        for block in self.dsl.split("\n\n"):
            
            dsl_scraper = DSLScraper(block)
            dsl_scrapers.append(dsl_scraper)
            
        return dsl_scrapers
        
        
class DSLScraper(object):
    
    def __init__(self, block):
        
        self.block = block
        
    def is_header(self, line):
        
        return ":" in line
    
    def parse(self):
        
        sentences = []
        
        for n, line in enumerate(self.block.split("\n")):
                
            if not line:
                continue
            
            if self.is_header(line):
                line = DSLHeaderLine(line, n)                
            else:
                line = DSLLine(line, n)
                
            sentences.append(line)
                
        return sentences


class DSLLine(object):
    """
        A DSL line abstraction
    """
        
    SEPARATOR = "->"
        
    def __init__(self, content, number):
                
        self.number = number
        self.content = content
        
    def parse(self):
        
        sentence = self.content.split(self.SEPARATOR)        
        
        if len(sentence) > 2:
            raise TemplateSyntaxError(self.number, "More than one '%s' token found in the same line" % self.SEPARATOR)
        elif len(sentence) < 2:
            raise TemplateSyntaxError(self.number, "Missed separator token '%s'" % self.SEPARATOR)
                       
        return [s.strip() for s in sentence]
    
    def is_header(self):
        
        return False
            

class DSLHeaderLine(DSLLine):
    
    SEPARATOR = ":"
    
    def is_header(self):
        
        return True        
