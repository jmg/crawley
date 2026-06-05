"""A simple parser interpreting the KISS-Crawley DSL."""

from crawley.simple_parser.compilers import DSLInterpreter
from crawley.simple_parser.parsers import DSLAnalizer


class Generator:
    """Generate entities and scrapers from a DSL template."""

    def __init__(self, dsl_template, settings):
        analizer = DSLAnalizer(dsl_template)
        code_blocks = analizer.parse()
        self.interpreter = DSLInterpreter(code_blocks, settings)

    def gen_entities(self):
        return self.interpreter.gen_entities()

    def gen_scrapers(self):
        return self.interpreter.gen_scrapers()


__all__ = ["Generator", "DSLAnalizer", "DSLInterpreter"]
