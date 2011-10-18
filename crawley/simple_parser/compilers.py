from crawley.scrapers import BaseScraper
from crawley.crawlers import BaseCrawler
from crawley.persistance.databases import Entity, Field, Unicode, setup, session, elixir
from crawley.persistance.connectors import connectors


class Interpreter(object):
    """
        This class "compiles" the DSL into scraper classes for
        the crawley framework
    """

    def __init__(self, code_blocks, settings):

        self.code_blocks = code_blocks
        self.settings = settings
        self.entities = {}

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
            matching_url = header.xpath                            

            attrs_dict = self._gen_scrape_method(block[1:])
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

        descriptors = {}
        fields = [line.field for lines in self.code_blocks for line in lines if not line.is_header]
        
        for field in fields:
            
            table = field["table"]
            column = field["column"]
            
            if table not in descriptors:
                descriptors[table] = [column, ]
            else:
                if column not in descriptors[table]:
                    descriptors[table].append(column)
                
        for entity_name, fields in descriptors.iteritems():
                        
            attrs_dict = dict([(field, Field(Unicode(255))) for field in fields])

            entity = self._gen_class(entity_name, (Entity, ), attrs_dict)
            self.entities[entity_name] = entity

        connector = connectors[self.settings.DATABASE_ENGINE](self.settings)

        elixir.metadata.bind = connector.get_connection_string()
        elixir.metadata.bind.echo = self.settings.SHOW_DEBUG_INFO

        setup(self.entities.values())

    def _gen_scrape_method(self, sentences):
        """
            Generates scrapers methods.
            Returns a dictionary containing methods and attributes for the
            scraper class.
        """
        entities = self.entities

        def scrape(self, response):
            """
                Generated scrape method
            """

            fields = {}                        
                        
            for sentence in sentences:
                                
                nodes = response.html.xpath(sentence.xpath)
                
                column = sentence.field["column"]
                table = sentence.field["table"]
                                                
                if nodes:
                                        
                    value = _get_text_recursive(nodes[0])
                    
                    if table not in fields:
                        fields[table] = {column : value}
                    else:
                        fields[table][column] = value
            
            for table, attrs_dict in fields.iteritems(): 
                
                entities[table](**attrs_dict)
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
