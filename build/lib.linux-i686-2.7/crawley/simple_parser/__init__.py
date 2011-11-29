"""
    A simple parser that interpretes the KISS_Crawley-BNF
"""

from parsers import DSLAnalizer
from compilers import DSLInterpreter


class Generator(object):
    
    def __init__(self, dsl_template, settings):
        
        analzier = DSLAnalizer(dsl_template)
        code_blocks = analzier.parse()
        self.interpreter = DSLInterpreter(code_blocks, settings)
    
    def gen_entities(self):
    
        return self.interpreter.gen_entities()

    def gen_scrapers(self):
    
        return self.interpreter.gen_scrapers()
