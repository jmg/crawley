"""
    A simple parser that interpretes the KISS_Crawley-BNF
"""

from parsers import DSLAnalizer
from compilers import Interpreter

def interprete(dsl, table_name, settings):
    
    analzier = DSLAnalizer(dsl)
    sentenses = analzier.parse_sentences()
    
    inerpreter = Interpreter(sentenses, table_name, settings)
    scraper = inerpreter.compile()
    return scraper
