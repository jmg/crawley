"""Smart scraper able to detect pages with a similar html structure."""

import difflib
from html.parser import HTMLParser

import httpx

from crawley.config import SIMILARITY_RATIO
from crawley.scrapers.base import BaseScraper


class SmartScraper(BaseScraper):
    """Scrape only pages whose html structure is similar to a template page.

    The structure of ``template_url`` is fetched once (synchronously) at
    construction time and every candidate page is compared against it.
    """

    template_url = None
    ratio = SIMILARITY_RATIO

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.template_url is None:
            raise ValueError(
                "%s must define a template_url attribute"
                % self.__class__.__name__
            )

        response = httpx.get(self.template_url, follow_redirects=True)
        self.template_html_schema = self._get_html_schema(response.text)

    def _validate(self, response):
        super()._validate(response)
        self._compare_with_template(response)

    def _compare_with_template(self, response):
        if self.debug:
            print("Evaluating similar html structure of %s" % response.url)

        html_schema = self._get_html_schema(response.raw_html)
        evaluated_ratio = difflib.SequenceMatcher(
            None, html_schema, self.template_html_schema
        ).ratio()

        if evaluated_ratio <= self.ratio:
            self.on_cannot_scrape(response)

    def _get_html_schema(self, html):
        schema = HtmlSchema()
        schema.feed(html)
        return schema.get_schema()


class HtmlSchema(HTMLParser):
    """Represents the structural skeleton of an html page (its tag sequence)."""

    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)

    def get_schema(self):
        return "/".join(self.tags)
