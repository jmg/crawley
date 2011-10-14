from crawley.exceptions import TemplateSyntaxError

class DSLAnalizer(object):
    """
        Analizes the DSL written by users
    """
    
    def __init__(self, dsl):
        
        self.dsl = dsl
        
    def is_header(self, line):
        
        return ":" in line
    
    def parse(self):
        
        blocks = []
        
        for line in self.dsl.split("\n"):
            
            lines = []
            
            if self.is_header(line):
                
                if lines:
                    blocks.append(lines)
                
                lines = []
                lines.append(DSLHeaderLine(line, n))
                
            else:
                lines.append(DSLLine(line, n))
                                        
        return blocks


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
