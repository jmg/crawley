"""Tests for the NoSQL sessions using fake drivers (no servers needed)."""

import sys
import types

import httpx


def test_mongo_session_commit(monkeypatch):
    from crawley.persistance.nosql import mongo

    mongo.mongo_objects.clear()
    inserted = []

    class FakeCollection:
        def insert_one(self, doc):
            inserted.append(doc)

    class FakeDB:
        def __getitem__(self, name):
            return FakeCollection()

    class FakeClient:
        def __init__(self, host):
            self.host = host

        def __getitem__(self, name):
            return FakeDB()

        def close(self):
            pass

    fake_pymongo = types.ModuleType("pymongo")
    fake_pymongo.MongoClient = FakeClient
    monkeypatch.setitem(sys.modules, "pymongo", fake_pymongo)

    settings = types.SimpleNamespace(
        MONGO_DB_HOST="mongodb://x", MONGO_DB_NAME="db", SHOW_DEBUG_INFO=False
    )
    mongo.mongo_session.set_up(settings, "MONGO_DB_HOST")

    class Pkg(mongo.MongoEntity):
        pass

    Pkg(name="crawley")
    mongo.mongo_session.commit()
    mongo.mongo_session.close()

    assert inserted == [{"name": "crawley"}]


def test_couch_session_commit(monkeypatch):
    from crawley.persistance.nosql import couch

    couch.couch_objects.clear()
    posted = []

    class FakeClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def put(self, path):
            pass

        def post(self, path, json):
            posted.append((path, json))

        def close(self):
            pass

    monkeypatch.setattr(httpx, "Client", FakeClient)

    settings = types.SimpleNamespace(
        COUCH_DB_HOST="http://x:5984", COUCH_DB_NAME="db", SHOW_DEBUG_INFO=False
    )
    couch.couch_session.set_up(settings, "COUCH_DB_HOST")

    class Pkg(couch.CouchEntity):
        pass

    Pkg(name="crawley")
    couch.couch_session.commit()
    couch.couch_session.close()

    assert posted == [("/db", {"name": "crawley"})]


def test_document_session_setup(tmp_path):
    from crawley.persistance.documents import json_session

    settings = types.SimpleNamespace(JSON_DOCUMENT=str(tmp_path / "x.json"))
    json_session.set_up(settings, "JSON_DOCUMENT")
    assert json_session.file_name == str(tmp_path / "x.json")


def test_csv_empty_commit(tmp_path):
    from crawley.persistance.documents import csv_doc, csv_session

    csv_doc.csv_objects.clear()
    csv_session.file_name = str(tmp_path / "empty.csv")
    csv_session.commit()
    assert open(csv_session.file_name).read() == ""
