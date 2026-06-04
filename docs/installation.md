# Installation

crawley requires **Python 3.9+**.

## From PyPI

```bash
pip install crawley
```

The core install pulls in `httpx`, `lxml`, `pyquery` and `cssselect` — enough
for crawling and the [scraping API](scraping.md).

## Optional extras

Some features need extra dependencies. Install only what you use:

| Extra      | Installs            | Enables                                    |
|------------|---------------------|--------------------------------------------|
| `sql`      | SQLAlchemy 2.x      | Relational persistence (SQLite/PG/MySQL)   |
| `mongo`    | pymongo             | MongoDB storage                            |
| `shell`    | IPython             | A nicer `crawley shell`                    |
| `gui`      | PySide6             | The visual scraping browser                |
| `http2`    | h2                  | HTTP/2 support in httpx                     |
| `dev`      | pytest, ruff, ...   | Running the test suite                     |
| `docs`     | mkdocs-material     | Building this documentation                |

```bash
pip install "crawley[sql]"
pip install "crawley[sql,mongo]"
```

## From source

```bash
git clone https://github.com/jmg/crawley
cd crawley
pip install -e ".[dev]"
pytest -q
```

## Building the docs

```bash
pip install -e ".[docs]"
mkdocs serve     # live preview on http://127.0.0.1:8000
mkdocs build     # static site in ./site
```
