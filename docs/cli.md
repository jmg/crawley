# CLI & Framework

Installing crawley provides a `crawley` command to scaffold and run projects.

## Commands

| Command                       | Description                                        |
|-------------------------------|----------------------------------------------------|
| `crawley startproject NAME`   | Scaffold a new project.                            |
| `crawley run`                 | Sync the database and run the project's crawlers.  |
| `crawley syncdb`              | Create the database from `models.py`.              |
| `crawley migratedb`           | Drop and recreate the tables.                      |
| `crawley shell URL`           | Fetch a url and open a Python shell to scrape it.  |
| `crawley browser URL`         | Open the visual scraping browser (needs `[gui]`).  |

`startproject` accepts a `-t/--type`: `code` (default), `template` (DSL) or
`database`.

## Project layout

```bash
crawley startproject myproject
cd myproject
```

```
myproject/
├── settings.py            # project configuration
└── myproject/
    ├── models.py          # your entities
    └── crawlers.py        # your crawlers + scrapers
```

### models.py

```python
from crawley.persistance import Entity, UrlEntity, Field, Unicode

class Package(Entity):
    package = Field(Unicode(255))
    description = Field(Unicode(255))
```

### crawlers.py

```python
from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper
from crawley.extractors import XPathExtractor
from models import *

class PackageScraper(BaseScraper):
    matching_urls = ["%"]

    def scrape(self, response):
        for row in response.css("div.package"):
            Package(package=row.css_first("h2::text"))

class PackageCrawler(BaseCrawler):
    start_urls = ["https://pypi.org/"]
    scrapers = [PackageScraper]
    max_depth = 1
    extractor = XPathExtractor
```

### settings.py

Relevant keys:

```python
DATABASE_ENGINE = "sqlite"       # sqlite, postgres, mysql, oracle
DATABASE_NAME = "myproject"
JSON_DOCUMENT = ""               # set a filename to dump JSON
XML_DOCUMENT = ""
CSV_DOCUMENT = ""
# MONGO_DB_HOST / MONGO_DB_NAME, COUCH_DB_HOST / COUCH_DB_NAME
MAX_CONCURRENCY = 100
SHOW_DEBUG_INFO = True
```

Then run:

```bash
crawley run
```

## The DSL (template projects)

For simple cases you can describe a scraper declaratively instead of writing
Python. Create a `template` project and write a `.crw` template:

```
PAGE => http://example.com/
packages.name -> /html/body//h2
packages.author -> /html/body//span[@class="author"]
```

- `PAGE => url` declares the template page (its structure is matched against
  candidate pages via `SmartScraper`).
- `table.column -> xpath` maps an XPath result to an entity column.

crawley compiles this into entities and scrapers at runtime. The companion
`config.ini` provides `start_urls` and `max_depth`:

```ini
[crawler]
start_urls = http://example.com/
max_depth = 1
```
