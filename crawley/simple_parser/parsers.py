from crawley.exceptions import TemplateSyntaxError

class DSLAnalizer(object):
    """
        Analizes the DSL written by users
    """
    
    def __init__(self, dsl):
        
        self.dsl = dsl
        
    def is_header(self, line):
        
        return DSLHeaderLine.SEPARATOR in line
        
    def parse(self):
        
        blocks = []
        lines = []
                
        for n, line in enumerate(self.dsl.split("\n")):
            
            line = line.strip()
            
            if not line:
                continue
            
            if self.is_header(line):
                
                if lines:
                    blocks.append(lines)
                
                lines = []
                lines.append(DSLHeaderLine(line, n))
                
            else:
                lines.append(DSLLine(line, n))
                    
        blocks.append(lines)
        return blocks


class DSLLine(object):
    """
        A DSL line abstraction
    """
        
    SEPARATOR = "->"    
    is_header = False
        
    def __init__(self, content, number):
                
        self.number = number
        self.content = content
        self._parse()
        
    def _parse(self):
        
        parts = self.content.split(self.SEPARATOR)        
        
        if len(parts) > 2:
            raise TemplateSyntaxError(self.number, "More than one '%s' token found in the same line" % self.SEPARATOR)
        elif len(parts) < 2:
            raise TemplateSyntaxError(self.number, "Missed separator token '%s'" % self.SEPARATOR)
        
        self.field = self._parse_attribs(parts[0])
        self.xpath = parts[1].strip()
        
    def _parse_attribs(self, parmas):
            
        table, column = parmas.split(".")
        return {"table" : table.strip(), "column" : column.strip()}


class DSLHeaderLine(DSLLine):
    
    SEPARATOR = "=>"
    is_header = True
    
    def _parse_attribs(self, field):
        
        return field
