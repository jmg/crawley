"""Example 4 — persisting scraped data to a JSON document.

Each ``Quote(...)`` instance becomes a row; the crawler commits the session as
it goes, and the session writes the file. Swap ``JSONDocument`` for
``CSVDocument`` / ``XMLDocument`` (or a SQLAlchemy ``Entity``) to change the
storage. See the *Persistence* page of the docs.

Run it::

    python examples/04_persistence_json.py
"""

from crawley.crawlers import BaseCrawler
from crawley.persistance.documents import JSONDocument, json_doc, json_session
from crawley.scrapers import BaseScraper

LIVE_SITE = "https://quotes.toscrape.com/"


class Quote(JSONDocument):
    pass


def crawl_to_json(base_url=LIVE_SITE, out_path="quotes.json"):
    """Crawl the quotes and dump them to *out_path*, returning the path."""
    # Reset the shared buffer so repeated runs start clean.
    json_doc.json_objects.clear()
    json_session.file_name = out_path

    class QuotesScraper(BaseScraper):
        matching_urls = ["%"]

        def scrape(self, response):
            for quote in response.css("div.quote"):
                Quote(
                    text=quote.css_first("span.text").text,
                    author=quote.css_first("small.author").text,
                )

        def get_urls(self, response):
            nxt = response.css_first("li.next a")
            return [nxt.attr("href")] if nxt else []

    class QuotesCrawler(BaseCrawler):
        start_urls = [base_url]
        scrapers = [QuotesScraper]
        search_all_urls = False
        requests_delay = 0
        requests_deviation = 0

    # Passing the session makes the crawler commit it after every scrape.
    QuotesCrawler(sessions=[json_session]).run()
    return out_path


if __name__ == "__main__":
    path = crawl_to_json()
    print("wrote", path)
