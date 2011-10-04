import utils

class SyntaxError(Exception):
    """
        DSL sintax errors
    """
        
    def __init__(self, line=0, *args, **kwargs):
    
        self.line = line
        Exception.__init__(self, *args, **kwargs)
        

class DSLAnalizer(object):
    """
        Analizes the DSL written by users
    """
    
    def __init__(self, dsl):
        
        self.dsl = dsl
    
    def _get_lines(self):
        
        return enumerate(utils.replace_escape_char(self.dsl).split("\n"))
        
    def parse_sentences(self):
        
        sentences = []
        
        for n, line in self._get_lines():
            line = DSLLine(line, n)
            sentences.append(line.parse())
            
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
            raise SyntaxError(self.number, "More than one '->' token found in the same line")
        elif len(sentence) < 2:            
            raise SyntaxError(self.number, "Missed separator token '->'")
        
        field, selector = sentence        
        return field.strip(), selector.strip()
        
