"""Examples of the modern crawley scraping API.

Run with:  python examples/modern_scraping.py
"""

import asyncio

from crawley.scraping import afetch_all, fetch, scrape


def one_off():
    """Scrape a single page with the high level API."""
    doc = fetch("https://quotes.toscrape.com/")

    print("Title:", doc.title)
    for quote in doc.css("div.quote"):
        text = quote.css_first("span.text").text
        author = quote.css_first("small.author").text
        tags = quote.css("a.tag::text")
        print(f"- {author}: {text} {tags}")

    print("Next page links:", doc.links("li.next a"))


def declarative():
    """Extract structured data declaratively."""
    data = scrape(
        "https://quotes.toscrape.com/",
        {
            "first_quote": "span.text::text",
            "first_author": "small.author::text",
            "all_authors": ["small.author::text"],
        },
    )
    print(data)


async def concurrent():
    """Fetch several pages at once."""
    urls = [f"https://quotes.toscrape.com/page/{n}/" for n in range(1, 4)]
    docs = await afetch_all(urls)
    for url, doc in zip(urls, docs):
        if doc is not None:
            print(url, "->", len(doc.css("div.quote")), "quotes")


if __name__ == "__main__":
    one_off()
    declarative()
    asyncio.run(concurrent())
