"""Tests for downloader middlewares."""


from crawley.http.response import Response
from crawley.middlewares import DownloaderMiddleware
from crawley.spider import Request, Spider


async def test_process_request_can_short_circuit(server):
    seen = []

    class FakeResponseMiddleware(DownloaderMiddleware):
        def process_request(self, request, spider):
            if request.url.endswith("/cached"):
                return Response(
                    raw_html="<html><body><h1>from middleware</h1></body></html>",
                    url=request.url,
                )
            return None

    class S(Spider):
        start_urls = [server + "/cached"]
        middlewares = [FakeResponseMiddleware]
        requests_delay = 0

        def parse(self, response):
            seen.append(response.css_first("h1").text)

    spider = S()
    await spider.start()
    assert seen == ["from middleware"]
    # No real request was made (short-circuited).
    assert spider.stats.get("requests", 0) == 0


async def test_process_request_headers_injection(server):
    captured = []

    class HeaderMiddleware(DownloaderMiddleware):
        def process_request(self, request, spider):
            request.headers["X-Test"] = "1"
            return None

    class S(Spider):
        start_urls = [server + "/page1"]
        middlewares = [HeaderMiddleware]
        requests_delay = 0

        def parse(self, response):
            captured.append(response.request.headers.get("X-Test"))

    await S().start()
    assert captured == ["1"]


async def test_process_response_chain(server):
    results = []

    class TagMiddleware(DownloaderMiddleware):
        def process_response(self, request, response, spider):
            response.tagged = True
            return response

    class S(Spider):
        start_urls = [server + "/page1"]
        middlewares = [TagMiddleware]
        requests_delay = 0

        def parse(self, response):
            results.append(getattr(response, "tagged", False))

    await S().start()
    assert results == [True]


async def test_process_request_reschedules():
    visited = []

    class RedirectMiddleware(DownloaderMiddleware):
        def process_request(self, request, spider):
            if request.url == "http://start/":
                return Request("http://target/", callback=spider.parse,
                               dont_filter=True)
            return Response(raw_html="<html></html>", url=request.url)

    class S(Spider):
        start_urls = ["http://start/"]
        middlewares = [RedirectMiddleware]
        requests_delay = 0

        def parse(self, response):
            visited.append(response.url)

    await S().start()
    assert visited == ["http://target/"]


async def test_process_exception_recovers():
    handled = []

    class RecoverMiddleware(DownloaderMiddleware):
        def process_exception(self, request, exception, spider):
            handled.append(type(exception).__name__)
            return Response(raw_html="<html><body>ok</body></html>",
                            url=request.url)

    class S(Spider):
        start_urls = ["http://127.0.0.1:1/down"]
        middlewares = [RecoverMiddleware]
        requests_delay = 0

        def parse(self, response):
            self.recovered = "ok" in response.raw_html

    spider = S()
    spider.request_manager.retry_policy.max_retries = 0
    await spider.start()
    assert handled and spider.recovered is True
