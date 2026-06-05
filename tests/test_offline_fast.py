"""Tests for OffLineCrawler / FastCrawler."""

from crawley.crawlers.fast import FastCrawler
from crawley.crawlers.offline import HTMLFixer, OffLineCrawler
from crawley.http.managers import FastRequestManager
from crawley.http.response import Response
from crawley.http.urls import UrlFinder


def test_html_fixer_rewrites_relative_assets():
    html = (
        '<html><body>'
        '<link href="style.css">'
        '<img src="img/logo.png">'
        '<img src="https://cdn.test/keep.png">'
        '</body></html>'
    )
    fixer = HTMLFixer(UrlFinder._url_regex, "http://site.test/dir", html)
    fixed = fixer.get_fixed_html()
    assert "http://site.test/dir/style.css" in fixed
    assert "http://site.test/dir/img/logo.png" in fixed
    # already-absolute urls are left untouched
    assert "https://cdn.test/keep.png" in fixed


def test_fast_crawler_uses_fast_manager():
    crawler = FastCrawler()
    assert isinstance(crawler.request_manager, FastRequestManager)


async def test_offline_crawler_fixes_response(monkeypatch):
    crawler = OffLineCrawler()
    html = '<html><body><link href="a.css"><img src="b.png"></body></html>'

    async def fake_make_request(url, data=None, extractor=None):
        return Response(
            raw_html=html,
            extracted_html=crawler.extractor.get_object(html),
            url=url,
        )

    monkeypatch.setattr(crawler.request_manager, "make_request", fake_make_request)

    response = await crawler._get_response("http://site.test/dir")
    assert "http://site.test/dir/a.css" in response.raw_html
    assert "http://site.test/dir/b.png" in response.raw_html
    await crawler.request_manager.aclose()
