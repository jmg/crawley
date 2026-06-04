"""Compile the parsed DSL into crawley scraper / crawler classes."""

from crawley.crawlers import BaseCrawler
from crawley.persistance.relational.databases import (
    Entity,
    Field,
    Unicode,
    session,
)
from crawley.scrapers import SmartScraper


class DSLInterpreter:
    """Turn DSL code blocks into runtime generated scraper classes."""

    def __init__(self, code_blocks, settings):
        self.code_blocks = code_blocks
        self.settings = settings
        self.entities = {}

    def gen_scrapers(self):
        """Return a list of runtime generated scraper classes."""
        scrapers = []

        for block in self.code_blocks:
            header = block[0]
            attrs_dict = self._gen_scrape_method(block[1:])
            attrs_dict["matching_urls"] = ["%"]
            attrs_dict["template_url"] = header.xpath

            scraper = self._gen_class(
                "GeneratedScraper", (SmartScraper,), attrs_dict
            )
            scrapers.append(scraper)

        return scrapers

    def _gen_class(self, name, bases, attrs_dict):
        return type(name, bases, attrs_dict)

    def gen_entities(self):
        """Generate the SQLAlchemy entity classes described by the DSL."""
        descriptors = {}
        fields = [
            line.field
            for lines in self.code_blocks
            for line in lines
            if not line.is_header
        ]

        for field in fields:
            table = field["table"]
            column = field["column"]
            descriptors.setdefault(table, [])
            if column not in descriptors[table]:
                descriptors[table].append(column)

        for entity_name, columns in descriptors.items():
            attrs_dict = {column: Field(Unicode(255)) for column in columns}
            entity = self._gen_class(entity_name, (Entity,), attrs_dict)
            self.entities[entity_name] = entity

        return list(self.entities.values())

    def _gen_scrape_method(self, sentences):
        """Build the ``scrape`` method for a generated scraper class."""
        entities = self.entities

        def _get_text_recursive(node):
            if node.text is not None and node.text.strip():
                return node.text
            for child in node.getchildren():
                return _get_text_recursive(child)
            return None

        def scrape(self, response):
            fields = {}

            for sentence in sentences:
                nodes = response.html.xpath(sentence.xpath)
                if not nodes:
                    continue

                column = sentence.field["column"]
                table = sentence.field["table"]
                value = _get_text_recursive(nodes[0])

                fields.setdefault(table, {})[column] = value

            for table, attrs_dict in fields.items():
                entities[table](**attrs_dict)
                session.commit()

        return {"scrape": scrape}


class CrawlerCompiler:
    """Compile a config and scrapers into a generated crawler class."""

    def __init__(self, scrapers, config):
        self.scrapers = scrapers
        self.config = config

    def compile(self):
        attrs_dict = {
            "scrapers": self.scrapers,
            "start_urls": self.config[("crawler", "start_urls")].split(","),
            "max_depth": int(self.config[("crawler", "max_depth")]),
        }
        return type("GeneratedCrawler", (BaseCrawler,), attrs_dict)
