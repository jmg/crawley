"""
Created on Oct 12, 2011

@author: fer
"""

import difflib

from base import BaseCrawler
from HTMLParser import HTMLParser
from htmllib import HTMLParseError


class SmartCrawler(BaseCrawler):
    """
        This class is used to find similar htmls
    """

    template_url = None
    ratio = 0.4

    def __init__(self, *args, **kwargs):

        BaseCrawler.__init__(self, *args, **kwargs)

        if self.template_url is None:
            raise ValueError

        self.template_html_schema = self.get_html_schema(self.request_manager.make_request(self.template_url, self.cookie_hanlder))

        if self.template_html_schema is None:
            raise ValueError

    def _validate_scraper(self, response, scraper_class):

        return BaseCrawler._validate_scraper(self, response, scraper_class) and self.compare_with_template(response)

    def compare_with_template(self, response):

        if self.debug :
            print "Evaluating similar html structure of %s" % response.url

        html_schema = self.get_html_schema(response.raw_html)

        if html_schema is None:

            if self.debug:
                print "Parse error reading: %s" % response.url

            return False

        evaluated_ratio = difflib.SequenceMatcher(None, html_schema.get_schema(), self.template_html_schema.get_schema()).ratio()

        return evaluated_ratio >= self.ratio

    def get_html_schema(self, html):

        try:
            html_schema = HtmlSchema()
            html_schema.feed(html)
            return html_schema

        except HTMLParseError:
            return None


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
