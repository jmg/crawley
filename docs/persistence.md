# Persistence

crawley can persist scraped data to relational databases, NoSQL stores or
plain documents. Sessions are passed to the crawler and committed as the crawl
progresses.

## Relational (SQLAlchemy 2.x)

Requires the `sql` extra (`pip install "crawley[sql]"`).

Define entities by subclassing `Entity`. Instantiating an entity stages it in
the shared session:

```python
from crawley.persistance import Entity, UrlEntity, Field, Unicode

class Package(Entity):
    package = Field(Unicode(255))
    description = Field(Unicode(255))

class Urls(UrlEntity):     # has href / parent columns
    pass
```

`Field` and `Unicode` are thin shims over SQLAlchemy's `Column` and column
types. Set up the engine and create the tables with `setup()`:

```python
from crawley.persistance import session, setup

setup("sqlite:///packages.sqlite")

Package(package="crawley", description="modern crawler")
session.commit()
```

Supported engines (via `crawley.persistance.relational.connectors`):
SQLite, PostgreSQL, MySQL, Oracle.

## Documents — JSON / XML / CSV

No extra dependencies. Subclass the document type; each instance becomes a row,
and the matching session writes the file on `commit()`:

```python
from crawley.persistance.documents import JSONDocument, json_session

class Quote(JSONDocument):
    pass

Quote(text="...", author="...")
json_session.file_name = "quotes.json"
json_session.commit()
```

`XMLDocument` / `xml_session` and `CSVDocument` / `csv_session` work the same
way.

## NoSQL — MongoDB / CouchDB

MongoDB requires the `mongo` extra; CouchDB talks to the HTTP API directly via
httpx.

```python
from crawley.persistance.nosql import MongoEntity, mongo_session

class Package(MongoEntity):
    pass

Package(name="crawley", stars=42)
# configured + committed by the crawler via settings (see CLI docs)
```

## Using sessions in a crawler

Pass the sessions you want committed to the crawler. After each successful
scrape, crawley calls `commit()` on every session:

```python
import asyncio
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.persistance.documents import JSONDocument, json_session

json_session.file_name = "out.json"

class Quote(JSONDocument):
    pass

class Scraper(BaseScraper):
    matching_urls = ["%"]
    def scrape(self, response):
        Quote(title=response.css_first("h1").text)

class Crawler(BaseCrawler):
    start_urls = ["https://quotes.toscrape.com/"]
    scrapers = [Scraper]

asyncio.run(Crawler(sessions=[json_session]).start())
```

When using the [CLI](cli.md), the storages are wired up automatically from your
`settings.py` (`DATABASE_*`, `JSON_DOCUMENT`, `MONGO_DB_HOST`, ...).
