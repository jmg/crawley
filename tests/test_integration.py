"""End-to-end integration: crawl + modern scraping API + persistence."""

import json

from crawley.crawlers import BaseCrawler
from crawley.scrapers import BaseScraper


async def test_crawl_persists_to_json(server, tmp_path):
    from crawley.persistance.documents import JSONDocument, json_doc, json_session

    json_doc.json_objects.clear()
    json_session.file_name = str(tmp_path / "out.json")

    class Row(JSONDocument):
        pass

    class Scraper(BaseScraper):
        matching_urls = ["%/page%"]

        def scrape(self, response):
            # Use the modern scraping shortcuts on the crawler response.
            Row(
                title=response.css_first("h1").text,
                author=response.css("p.author::text")[0],
            )

    class Crawler(BaseCrawler):
        start_urls = [server + "/"]
        scrapers = [Scraper]
        max_depth = 1
        requests_delay = 0
        requests_deviation = 0

    crawler = Crawler(sessions=[json_session])
    await crawler.start()

    data = json.load(open(json_session.file_name))
    titles = {row["title"] for row in data}
    assert any("Title 1" == t for t in titles)
    assert all("author" in row for row in data)
