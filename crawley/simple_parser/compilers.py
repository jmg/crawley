import types
from crawley.scrapers import BaseScraper
from crawley.crawlers import BaseCrawler
from crawley.persistance.databases import Entity, Field, Unicode, setup, session, elixir
from crawley.persistance.connectors import SqliteConnector


class Interpreter(object):
    """
        This class "compiles" the DSL into scraper classes for
        the crawley framework
    """

    def __init__(self, code_blocks, settings):

        self.code_blocks = code_blocks
        self.settings = settings

    def compile(self):
        """
            Returns a runtime generated scraper class
        """
        self._gen_entities()
        return self._gen_scrapers()

    def _gen_scrapers(self):

        scrapers = []

        for block in self.code_blocks:

            header = block[0]
            entity_name, matching_url = header

            attrs_dict = self._gen_scrape_method(self.entities[entity_name], block[1:])
            attrs_dict["matching_urls"] = [matching_url, ]

            scraper = self._gen_class("GeneratedScraper", (BaseScraper, ), attrs_dict)
            scrapers.append(scraper)

        return scrapers

    def _gen_class(self, name, bases, attrs_dict):
        """
            Generates a class at runtime
        """

        return type(name, bases, attrs_dict)

    def _gen_entities(self):
        """
            Generates the entities classes
        """

        self.entities = {}

        for block in self.code_blocks:

            header = block[0]
            entity_name = header[0]

            self.fields = [s[0] for s in block[1:]]
            attrs_dict = dict([(field, Field(Unicode(255))) for field in self.fields])

            entity = self._gen_class(entity_name, (Entity, ), attrs_dict)
            self.entities[entity_name] = entity

        connector = SqliteConnector(self.settings)

        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO

        setup(self.entities.values())

    def _gen_scrape_method(self, entity, sentences):
        """
            Generates scrapers methods.
            Returns a dictionary containing methods and attributes for the
            scraper class.
        """

        def scrape(self, response):
            """
                Generated scrape method
            """

            fields = {}

            for field, selector in sentences:

                nodes = response.html.xpath(selector)
                if nodes:
                    fields[field] = _get_text_recursive(nodes[0])

            entity(**fields)
            session.commit()


        def _get_text_recursive(node):
            """
                Extract the text from html nodes recursively.
            """
            if node.text is not None and node.text.strip():
                return node.text

            childs = node.getchildren()

            for child in childs:
                return _get_text_recursive(child)

        return { "scrape" : scrape }



class CrawlerCompiler(object):

    def __init__(self, config, scrapers):

        self.scrapers = scrapers
        self.config = config

    def compile(self):

        attrs_dict = {}
        attrs_dict["scrapers"] = self.scrapers
        attrs_dict["max_depth"] = self.config.max_depth
        attrs_dict["start_urls"] = self.config.start_urls

        return type("GeneratedCrawler", (BaseCrawler, ), attrs_dict)
