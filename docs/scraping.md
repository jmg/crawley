# Scraping API

The `crawley.scraping` module is the high-level, ergonomic entry point for
"just scrape this page" use cases. It is built on the same `httpx` + `lxml`
stack as the crawler but gives you a friendly, `parsel` / `requests-html`
flavoured interface.

## Fetching a page

```python
from crawley.scraping import fetch

doc = fetch("https://quotes.toscrape.com/")   # returns a Document
```

`fetch()` is synchronous. For async code use `afetch()`, and to fetch many
pages concurrently use `afetch_all()`:

```python
import asyncio
from crawley.scraping import afetch, afetch_all

doc = asyncio.run(afetch("https://example.com"))

urls = ["https://example.com/1", "https://example.com/2"]
docs = asyncio.run(afetch_all(urls))   # list of Document (None on error)
```

You can also parse html you already have:

```python
from crawley.scraping import parse

doc = parse("<html>...</html>", url="https://example.com/")
```

## Selecting elements

A `Document` (and any `Element`) supports CSS selectors and XPath:

```python
doc.css("div.quote")          # -> list[Element]
doc.css_first("h1")           # -> Element | None
doc.xpath("//h1/text()")      # -> list (strings or Element)
doc.title                     # -> the <title> text
```

Queries can be nested:

```python
for quote in doc.css("div.quote"):
    text = quote.css_first("span.text").text
    author = quote.css_first("small.author").text
    tags = quote.css("a.tag::text")
```

### Pseudo-selectors

Append `::text` or `::attr(name)` to a CSS selector to pull values instead of
elements (just like scrapy / parsel):

```python
doc.css("span.text::text")    # -> ["The quote", ...]
doc.css("a::attr(href)")      # -> ["https://...", ...]  (absolute)
```

### Element helpers

```python
el = doc.css_first("a")
el.text                       # normalized recursive text
el.attr("href")               # attribute (or a default)
el.attrs                      # dict of all attributes
el.html                       # serialized back to html
```

### Links

`links()` returns the de-duplicated, **absolute** hrefs on the page:

```python
doc.links()                   # all <a href>
doc.links("li.next a")        # only matching a chosen selector
```

!!! note "Absolute urls"
    When a `url` is provided (`fetch` does this automatically), relative links
    are resolved to absolute urls, so `href="page2"` becomes
    `https://site/dir/page2`.

## Declarative extraction

`extract()` maps field names to selectors. A **string** selector yields a
single value (the first match); a **one-element list** selector yields the
list of every match:

```python
doc.extract({
    "title":   "h1::text",
    "price":   "span.price::text",
    "images":  ["img::attr(src)"],
    "authors": ["small.author::text"],
})
# {"title": "...", "price": "...", "images": [...], "authors": [...]}
```

`scrape()` fetches and extracts in a single call:

```python
from crawley.scraping import scrape

data = scrape("https://example.com", {"title": "h1::text"})
```

## Inside a crawler

The same shortcuts are available on the crawler's `response` object, so you can
use the modern API inside a scraper's `scrape()` method:

```python
class MyScraper(BaseScraper):
    matching_urls = ["%"]

    def scrape(self, response):
        response.css_first("h1").text
        response.css("a::attr(href)")
        response.extract({"title": "h1::text"})
        response.doc            # the underlying Document
```
