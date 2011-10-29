import difflib

from HTMLParser import HTMLParser

from base import BaseScraper
from crawley.http.managers import FastRequestManager
from crawley.exceptions import ScraperCantParseError
from crawley.config import SIMILARITY_RATIO


class SmartScraper(BaseScraper):
    """
        This class is used to find similar htmls
    """

    template_url = None
    ratio = SIMILARITY_RATIO

    def __init__(self, *args, **kwargs):

        BaseScraper.__init__(self, *args, **kwargs)

        if self.template_url is None:
            raise ValueError("%s must have a template_url attribute" % self.__class__.__name__)

        self.request_manager = FastRequestManager()
        response = self.request_manager.make_request(self.template_url)
        self.template_html_schema = self._get_html_schema(response.raw_html)

    def _validate(self, response):

        return BaseScraper._validate(self, response) and self._compare_with_template(response)

    def _compare_with_template(self, response):

        if self.debug :
            print "Evaluating similar html structure of %s" % response.url

        html_schema = self._get_html_schema(response.raw_html)

        evaluated_ratio = difflib.SequenceMatcher(None, html_schema, self.template_html_schema).ratio()

        if evaluated_ratio <= self.ratio:
            self.on_cannot_scrape(response)

    def _get_html_schema(self, html):

        html_schema = HtmlSchema()
        html_schema.feed(html)
        return html_schema.get_schema()


class HtmlSchema(HTMLParser):
    """
        This class represents an html page structure, used to compare with another pages
    """

    def __init__(self):
        self.tags = []
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def get_schema(self):
        return "/".join(self.tags)
