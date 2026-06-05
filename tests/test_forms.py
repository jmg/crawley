"""Tests for FormRequest.from_response."""

import pytest

from crawley.http.response import Response
from crawley.spider import FormRequest, Spider


def test_from_response_post_prefills_inputs():
    html = (
        '<form action="/submit" method="post">'
        '<input name="user" value="bob">'
        '<input name="token" value="xyz">'
        '<input name="pass" type="password">'
        '<input type="submit" value="go">'
        "</form>"
    )
    resp = Response(raw_html=html, url="http://site.test/login")
    req = FormRequest.from_response(resp, formdata={"pass": "secret"})

    assert isinstance(req, FormRequest)
    assert req.method == "POST"
    assert req.url == "http://site.test/submit"
    assert req.data == {"user": "bob", "token": "xyz", "pass": "secret"}


def test_from_response_get_builds_querystring():
    html = '<form action="/search" method="get"><input name="q" value=""></form>'
    resp = Response(raw_html=html, url="http://site.test/")
    req = FormRequest.from_response(resp, formdata={"q": "crawley"})

    assert req.method == "GET"
    assert "q=crawley" in req.url
    assert req.data is None


def test_from_response_select_and_textarea():
    html = (
        '<form action="/x" method="post">'
        '<select name="cat"><option value="a">A</option>'
        '<option value="b" selected>B</option></select>'
        '<textarea name="msg">hi</textarea>'
        "</form>"
    )
    resp = Response(raw_html=html, url="http://site.test/")
    req = FormRequest.from_response(resp)
    assert req.data == {"cat": "b", "msg": "hi"}


def test_from_response_no_form_raises():
    resp = Response(raw_html="<html><body>no form</body></html>", url="http://x/")
    with pytest.raises(ValueError):
        FormRequest.from_response(resp)


async def test_formrequest_end_to_end(server):
    captured = []

    class LoginSpider(Spider):
        start_urls = [server + "/login-form"]
        requests_delay = 0

        def parse(self, response):
            yield FormRequest.from_response(
                response, formdata={"pass": "secret"}, callback=self.after
            )

        def after(self, response):
            captured.append(response.raw_html)

    await LoginSpider().start()

    body = captured[0]
    assert "user=bob" in body
    assert "pass=secret" in body
