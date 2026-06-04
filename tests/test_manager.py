"""Tests for the management commands and project types."""

import os
import sqlite3
import sys
import types

import pytest

from crawley.manager.commands.startproject import StartProjectCommand


def test_startproject_template_type(tmp_path):
    cmd = StartProjectCommand(
        ["-t", "template", "tmpl"], base_dir=str(tmp_path)
    )
    cmd.checked_execute()

    base = os.path.join(tmp_path, "tmpl")
    assert os.path.exists(os.path.join(base, "settings.py"))
    assert os.path.exists(os.path.join(base, "tmpl", "template.crw"))
    assert os.path.exists(os.path.join(base, "tmpl", "config.ini"))


def test_startproject_requires_name():
    with pytest.raises(SystemExit):
        StartProjectCommand([]).checked_execute()


def _settings(tmp_path, db_name):
    inner = tmp_path / "proj"
    inner.mkdir(exist_ok=True)
    (inner / "__init__.py").write_text("")
    return types.SimpleNamespace(
        PATH=str(tmp_path),
        PROJECT_NAME="proj",
        PROJECT_ROOT=str(inner),
        PROJECT_TYPE="code",
        DATABASE_ENGINE="sqlite",
        DATABASE_NAME=db_name,
        DATABASE_USER="",
        DATABASE_PASSWORD="",
        DATABASE_HOST="",
        DATABASE_PORT="",
        SHOW_DEBUG_INFO=False,
    )


@pytest.fixture
def clean_modules():
    for name in ("models", "crawlers", "settings"):
        sys.modules.pop(name, None)
    yield
    for name in ("models", "crawlers", "settings"):
        sys.modules.pop(name, None)


def test_syncdb_creates_sqlite(tmp_path, clean_modules):
    pytest.importorskip("sqlalchemy")
    from crawley.manager.commands.syncdb import SyncDbCommand
    from crawley.utils import add_to_path

    settings = _settings(tmp_path, "syncdb_db")
    (tmp_path / "proj" / "models.py").write_text(
        "from crawley.persistance import Entity, Field, Unicode\n"
        "class SyncRow(Entity):\n"
        "    name = Field(Unicode(255))\n"
    )
    add_to_path(settings.PROJECT_ROOT, 1)

    SyncDbCommand(settings=settings).checked_execute()

    db_file = os.path.join(tmp_path, "syncdb_db.sqlite")
    assert os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    tables = {
        row[0]
        for row in conn.execute("select name from sqlite_master where type='table'")
    }
    conn.close()
    assert "syncrow" in tables


def test_migratedb_recreates_tables(tmp_path, clean_modules):
    pytest.importorskip("sqlalchemy")
    from crawley.manager.commands.migratedb import MigrateDbCommand
    from crawley.utils import add_to_path

    settings = _settings(tmp_path, "migrate_db")
    (tmp_path / "proj" / "models.py").write_text(
        "from crawley.persistance import Entity, Field, Unicode\n"
        "class MigrateRow(Entity):\n"
        "    name = Field(Unicode(255))\n"
    )
    add_to_path(settings.PROJECT_ROOT, 1)

    MigrateDbCommand(settings=settings).checked_execute()

    db_file = os.path.join(tmp_path, "migrate_db.sqlite")
    assert os.path.exists(db_file)
    conn = sqlite3.connect(db_file)
    tables = {
        row[0]
        for row in conn.execute("select name from sqlite_master where type='table'")
    }
    conn.close()
    assert "migraterow" in tables


def test_unknown_command_exits():
    from crawley.manager import run_cmd

    with pytest.raises(SystemExit):
        run_cmd(["crawley", "not-a-command"])


def test_no_command_exits():
    from crawley.manager import run_cmd

    with pytest.raises(SystemExit):
        run_cmd(["crawley"])
