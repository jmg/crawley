"""Example 2 — a crawler that follows pagination.

Defines a ``BaseScraper`` (data extraction) and a ``BaseCrawler`` (navigation).
The scraper returns the "next" link from ``get_urls`` so the crawler walks
every page. ``search_all_urls = False`` keeps it focused on that single link
instead of following every ``<a>`` on the page.

Run it::

    python examples/02_crawler.py
"""

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper

LIVE_SITE = "https://quotes.toscrape.com/"


def crawl_quotes(base_url=LIVE_SITE):
    """Crawl every page and return the collected quotes."""
    collected = []

    class QuotesScraper(BaseScraper):
        matching_urls = ["%"]  # scrape every page we visit

        def scrape(self, response):
            for quote in response.css("div.quote"):
                collected.append(
                    {
                        "text": quote.css_first("span.text").text,
                        "author": quote.css_first("small.author").text,
                    }
                )

        def get_urls(self, response):
            # Follow the pagination link, if there is one.
            nxt = response.css_first("li.next a")
            return [nxt.attr("href")] if nxt else []

    class QuotesCrawler(BaseCrawler):
        start_urls = [base_url]
        scrapers = [QuotesScraper]
        search_all_urls = False  # only follow the link the scraper returns
        requests_delay = 0
        requests_deviation = 0

    QuotesCrawler().run()
    return collected


if __name__ == "__main__":
    quotes = crawl_quotes()
    print(f"Collected {len(quotes)} quotes")
    for quote in quotes:
        print(f"- {quote['author']}: {quote['text']}")
