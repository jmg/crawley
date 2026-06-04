"""Tests for the SMTP mail sender (no real network)."""

import smtplib

import pytest

from crawley.smtp.sender import MailSender


class FakeSMTP:
    instances = []

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sent = []
        self.tls_started = False
        self.logged_in = None
        FakeSMTP.instances.append(self)

    def ehlo(self):
        pass

    def starttls(self):
        self.tls_started = True

    def login(self, user, password):
        self.logged_in = (user, password)

    def send_message(self, msg):
        self.sent.append(msg)

    def quit(self):
        pass


@pytest.fixture(autouse=True)
def _patch_smtp(monkeypatch):
    FakeSMTP.instances = []
    monkeypatch.setattr(smtplib, "SMTP", FakeSMTP)
    yield


def test_send_builds_message():
    sender = MailSender("smtp.test", enable_ssl=False)
    sender.send(["a@test.com", "b@test.com"], "hello body", subject="Hi")

    server = sender.server
    assert len(server.sent) == 1
    msg = server.sent[0]
    assert msg["To"] == "a@test.com, b@test.com"
    assert msg["Subject"] == "Hi"
    assert "hello body" in msg.get_content()


def test_from_address_defaults_to_user():
    sender = MailSender("smtp.test", user="me@test.com", enable_ssl=False)
    sender.send(["x@test.com"], "body")
    assert sender.server.sent[0]["From"] == "me@test.com"


def test_ssl_flow_authenticates():
    sender = MailSender(
        "smtp.test", user="u", password="p", enable_ssl=True
    )
    assert sender.server.tls_started is True
    assert sender.server.logged_in == ("u", "p")
