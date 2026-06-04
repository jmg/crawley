"""Example 5 — fetching many pages concurrently.

``afetch_all`` fetches a list of urls at the same time and returns a list of
``Document`` objects (``None`` for any url that failed), all on a single
``httpx.AsyncClient``.

Run it::

    python examples/05_concurrent_fetch.py
"""

import asyncio

from crawley.scraping import afetch_all

LIVE_SITE = "https://quotes.toscrape.com/"


async def count_quotes_per_page(base_url=LIVE_SITE, pages=3):
    """Fetch several pages at once and count the quotes on each."""
    base = base_url if base_url.endswith("/") else base_url + "/"
    urls = [base] + [f"{base}page/{n}/" for n in range(2, pages + 1)]
    docs = await afetch_all(urls)

    counts = {}
    for url, doc in zip(urls, docs):
        counts[url] = len(doc.css("div.quote")) if doc is not None else 0
    return counts


if __name__ == "__main__":
    for url, count in asyncio.run(count_quotes_per_page()).items():
        print(f"{count:>3}  {url}")
