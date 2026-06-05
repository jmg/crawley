"""Tests for visited-url de-duplication."""

import asyncio

from crawley.crawlers import BaseCrawler


def _counting_crawler(server, **attrs):
    fetched = []

    class C(BaseCrawler):
        requests_delay = 0
        requests_deviation = 0

        def _manage_scrapers(self, response):
            fetched.append(response.url)
            return super()._manage_scrapers(response)

    for key, value in attrs.items():
        setattr(C, key, value)
    return C, fetched


async def test_unique_urls_dedupes(server):
    C, fetched = _counting_crawler(
        server, start_urls=[server + "/page1", server + "/page1"], max_depth=0
    )
    await C().start()
    assert len(fetched) == 1


async def test_unique_urls_can_be_disabled(server):
    C, fetched = _counting_crawler(
        server,
        start_urls=[server + "/page1", server + "/page1"],
        max_depth=0,
        unique_urls=False,
    )
    await C().start()
    assert len(fetched) == 2


async def test_cycle_terminates(server):
    """With unbounded depth, only de-duplication prevents an infinite loop."""
    C, fetched = _counting_crawler(
        server, start_urls=[server + "/loop-a"], max_depth=-1
    )
    await asyncio.wait_for(C().start(), timeout=5)

    visited = {url.rsplit("/", 1)[-1] for url in fetched}
    assert visited == {"loop-a", "loop-b"}
    assert len(fetched) == 2
