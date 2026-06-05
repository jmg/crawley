"""Example 3 — crawling politely.

Shows the politeness knobs: honour ``robots.txt``, throttle requests per host
and retry transient failures with exponential backoff. See the *Politeness*
page of the docs for the full list.

Run it::

    python examples/03_polite_crawler.py
"""

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper

LIVE_SITE = "https://quotes.toscrape.com/"


def crawl_politely(base_url=LIVE_SITE):
    """Crawl the first two pages respecting robots.txt and rate limits."""
    collected = []
    blocked = []

    class QuotesScraper(BaseScraper):
        matching_urls = ["%"]

        def scrape(self, response):
            for quote in response.css("div.quote"):
                collected.append(quote.css_first("span.text").text)

        def get_urls(self, response):
            nxt = response.css_first("li.next a")
            return [nxt.attr("href")] if nxt else []

    class PoliteCrawler(BaseCrawler):
        start_urls = [base_url]
        scrapers = [QuotesScraper]
        search_all_urls = False

        # --- politeness ---
        respect_robots = True             # obey robots.txt (+ Crawl-delay)
        crawl_delay = 0.0                 # min seconds between same-host requests
        max_concurrency_per_host = 4      # at most N concurrent requests per host
        max_retries = 3                   # retry 429/5xx + network errors...
        retry_backoff = 0.2               # ...with exponential backoff + jitter

        def on_robots_blocked(self, url):
            blocked.append(url)

    PoliteCrawler().run()
    return collected, blocked


if __name__ == "__main__":
    quotes, blocked = crawl_politely()
    print(f"Collected {len(quotes)} quotes, {len(blocked)} urls blocked by robots")
