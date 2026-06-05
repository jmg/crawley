"""Example 1 — the high level scraping API.

Pull data out of a single page with ``crawley.scraping``: ``fetch`` returns a
``Document`` you can query with CSS selectors / XPath and extract declaratively.

Run it against the live site::

    python examples/01_scraping_quickstart.py

Every function takes a ``base_url`` so the examples are also exercised by the
test suite against a local server.
"""

from crawley.scraping import fetch

LIVE_SITE = "https://quotes.toscrape.com/"


def list_quotes(base_url=LIVE_SITE):
    """Return ``[{text, author, tags}, ...]`` for the quotes on the page."""
    doc = fetch(base_url)

    quotes = []
    for quote in doc.css("div.quote"):
        quotes.append(
            {
                "text": quote.css_first("span.text").text,
                "author": quote.css_first("small.author").text,
                "tags": quote.css("a.tag::text"),
            }
        )
    return quotes


def page_summary(base_url=LIVE_SITE):
    """Use declarative ``extract`` to summarize a page in one call."""
    return fetch(base_url).extract(
        {
            "title": "h1::text",
            "first_quote": "span.text::text",
            "authors": ["small.author::text"],
        }
    )


def next_page_link(base_url=LIVE_SITE):
    """Return the absolute url of the 'next' page (or ``None``)."""
    nxt = fetch(base_url).css_first("li.next a")
    return nxt.attr("href") if nxt else None


if __name__ == "__main__":
    for quote in list_quotes():
        print(f"{quote['author']}: {quote['text']}  {quote['tags']}")
    print("\nsummary:", page_summary())
    print("next page:", next_page_link())
