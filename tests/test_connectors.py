"""Tests for the relational database connectors."""

import types

import pytest

pytest.importorskip("sqlalchemy")

from crawley.persistance.relational.connectors import connectors


def _settings(**kw):
    return types.SimpleNamespace(**kw)


def test_sqlite_connection_string():
    settings = _settings(
        DATABASE_ENGINE="sqlite", DATABASE_NAME="db.sqlite", PATH="/tmp"
    )
    conn = connectors["sqlite"](settings)
    assert conn.get_connection_string() == "sqlite:////tmp/db.sqlite"


def test_postgres_connection_string():
    settings = _settings(
        DATABASE_ENGINE="postgres",
        DATABASE_NAME="mydb",
        DATABASE_USER="u",
        DATABASE_PASSWORD="p",
        DATABASE_HOST="localhost",
        DATABASE_PORT="5432",
    )
    conn = connectors["postgres"](settings)
    assert conn.get_connection_string() == "postgresql://u:p@localhost:5432/mydb"


def test_mysql_connection_string():
    settings = _settings(
        DATABASE_ENGINE="mysql",
        DATABASE_NAME="mydb",
        DATABASE_USER="u",
        DATABASE_PASSWORD="p",
        DATABASE_HOST="localhost",
        DATABASE_PORT="3306",
    )
    conn = connectors["mysql"](settings)
    assert conn.get_connection_string() == "mysql://u:p@localhost:3306/mydb"


def test_unknown_engine_exits():
    with pytest.raises(SystemExit):
        connectors["nope"]
