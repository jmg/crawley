from crawley.exceptions import TemplateSyntaxError

class DSLAnalizer(object):
    """
        Analizes the DSL written by users
    """
    
    def __init__(self, dsl):
        
        self.dsl = dsl
    
    def parse_sentences(self):
        
        sentences = []
        
        for n, line in enumerate(self.dsl.split("\n")):
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
            raise TemplateSyntaxError(self.number, "More than one '->' token found in the same line")
        elif len(sentence) < 2:            
            raise TemplateSyntaxError(self.number, "Missed separator token '->'")
        
        field, selector = sentence        
        return field.strip(), selector.strip()
        
