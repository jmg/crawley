"""
    A simple parser that interpretes the KISS_Crawley-BNF
"""

from parsers import DSLAnalizer
from compilers import Interpreter

def interprete(dsl, settings):
    
    analzier = DSLAnalizer(dsl)
    code_blocks = analzier.parse()
    
    interpreter = Interpreter(code_blocks, settings)    
    scrapers = interpreter.compile()
    return scrapers
