"""Run the documentation examples against the local quotes server.

This keeps every example in ``examples/`` honest: if an example breaks, its
test fails. Examples are loaded by path (their filenames start with a digit, so
they aren't importable as normal modules).
"""

import importlib.util
import json
import pathlib

import pytest

EXAMPLES_DIR = pathlib.Path(__file__).resolve().parent.parent / "examples"

# A fresh quotes site has 3 pages x 2 quotes.
TOTAL_QUOTES = 6


def load_example(filename):
    path = EXAMPLES_DIR / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# -- 01 scraping quickstart -------------------------------------------------


def test_quickstart_list_quotes(quotes_server):
    mod = load_example("01_scraping_quickstart.py")
    quotes = mod.list_quotes(quotes_server)
    assert len(quotes) == 2  # first page
    assert quotes[0]["text"] == "Quote 1-1"
    assert quotes[0]["author"] == "Author 11"
    assert "common" in quotes[0]["tags"]


def test_quickstart_summary(quotes_server):
    mod = load_example("01_scraping_quickstart.py")
    summary = mod.page_summary(quotes_server)
    assert summary["title"] == "Quotes to Scrape"
    assert summary["first_quote"] == "Quote 1-1"
    assert summary["authors"] == ["Author 11", "Author 12"]


def test_quickstart_next_link(quotes_server):
    mod = load_example("01_scraping_quickstart.py")
    assert mod.next_page_link(quotes_server) == quotes_server + "page/2/"


# -- 02 crawler -------------------------------------------------------------


def test_crawler_follows_pagination(quotes_server):
    mod = load_example("02_crawler.py")
    quotes = mod.crawl_quotes(quotes_server)
    assert len(quotes) == TOTAL_QUOTES
    authors = {q["author"] for q in quotes}
    assert {"Author 11", "Author 21", "Author 31"} <= authors


# -- 03 polite crawler ------------------------------------------------------


def test_polite_crawler(quotes_server):
    mod = load_example("03_polite_crawler.py")
    collected, blocked = mod.crawl_politely(quotes_server)
    assert len(collected) == TOTAL_QUOTES
    assert blocked == []  # robots.txt allows everything here


# -- 04 persistence ---------------------------------------------------------


def test_persistence_json(quotes_server, tmp_path):
    mod = load_example("04_persistence_json.py")
    out = str(tmp_path / "quotes.json")
    path = mod.crawl_to_json(quotes_server, out)

    data = json.load(open(path))
    assert len(data) == TOTAL_QUOTES
    assert all("text" in row and "author" in row for row in data)


# -- 05 concurrent ----------------------------------------------------------


async def test_concurrent_fetch(quotes_server):
    mod = load_example("05_concurrent_fetch.py")
    counts = await mod.count_quotes_per_page(quotes_server, pages=3)
    assert len(counts) == 3
    assert all(count == 2 for count in counts.values())


# -- every example at least imports cleanly ---------------------------------


@pytest.mark.parametrize(
    "filename",
    [
        "01_scraping_quickstart.py",
        "02_crawler.py",
        "03_polite_crawler.py",
        "04_persistence_json.py",
        "05_concurrent_fetch.py",
    ],
)
def test_example_imports(filename):
    assert load_example(filename) is not None
