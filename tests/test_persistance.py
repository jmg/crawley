"""Tests for the persistence layer (documents + relational)."""

import json
import os

import pytest


def test_json_document(tmp_path):
    from crawley.persistance.documents import JSONDocument, json_session
    from crawley.persistance.documents import json_doc

    json_doc.json_objects.clear()

    class Row(JSONDocument):
        pass

    Row(name="a", value="1")
    Row(name="b", value="2")

    json_session.file_name = os.path.join(tmp_path, "data.json")
    json_session.commit()

    data = json.load(open(json_session.file_name))
    assert {"name": "a", "value": "1"} in data
    assert len(data) == 2


def test_csv_document(tmp_path):
    from crawley.persistance.documents import CSVDocument, csv_session
    from crawley.persistance.documents import csv_doc

    csv_doc.csv_objects.clear()

    class Row(CSVDocument):
        pass

    Row(name="a", value="1")

    csv_session.file_name = os.path.join(tmp_path, "data.csv")
    csv_session.commit()

    content = open(csv_session.file_name).read()
    assert "name" in content and "a" in content


def test_xml_document(tmp_path):
    from crawley.persistance.documents import XMLDocument, xml_session

    class Row(XMLDocument):
        pass

    Row(name="a")
    xml_session.file_name = os.path.join(tmp_path, "data.xml")
    xml_session.commit()

    assert os.path.exists(xml_session.file_name)
    assert b"<Row>" in open(xml_session.file_name, "rb").read()


def test_relational_entity():
    pytest.importorskip("sqlalchemy")
    from crawley.persistance.relational.databases import (
        Entity,
        Field,
        Unicode,
        session,
        setup,
    )

    class Package(Entity):
        package = Field(Unicode(255))
        author = Field(Unicode(255))

    setup("sqlite:///:memory:")

    Package(package="crawley", author="jmg")
    Package(package="httpx", author="encode")
    session.commit()

    rows = session.query(Package).all()
    assert {r.package for r in rows} == {"crawley", "httpx"}
    session.remove()
