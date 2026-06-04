"""Integration tests for the management commands."""

import importlib
import os
import sqlite3
import sys

import pytest

from crawley.manager.commands.startproject import StartProjectCommand


def test_startproject(tmp_path):
    cmd = StartProjectCommand(["demo"], base_dir=str(tmp_path))
    cmd.checked_execute()

    base = os.path.join(tmp_path, "demo")
    assert os.path.exists(os.path.join(base, "settings.py"))
    assert os.path.exists(os.path.join(base, "demo", "models.py"))
    assert os.path.exists(os.path.join(base, "demo", "crawlers.py"))


@pytest.fixture
def _clean_user_modules():
    names = ["settings", "models", "crawlers"]
    for name in names:
        sys.modules.pop(name, None)
    yield
    for name in names:
        sys.modules.pop(name, None)


def test_run_command_end_to_end(tmp_path, server, _clean_user_modules):
    pytest.importorskip("sqlalchemy")
    from crawley.utils import add_to_path

    project = tmp_path / "proj"
    inner = project / "proj"
    inner.mkdir(parents=True)

    db_path = str(tmp_path / "cmddb")

    (project / "settings.py").write_text(
        "import os\n"
        "PATH = os.path.dirname(os.path.abspath(__file__))\n"
        "PROJECT_NAME = 'proj'\n"
        "PROJECT_ROOT = os.path.join(PATH, 'proj')\n"
        "PROJECT_TYPE = 'code'\n"
        "DATABASE_ENGINE = 'sqlite'\n"
        "DATABASE_NAME = %r\n"
        "DATABASE_USER = DATABASE_PASSWORD = DATABASE_HOST = DATABASE_PORT = ''\n"
        "SHOW_DEBUG_INFO = False\n" % db_path
    )
    (inner / "__init__.py").write_text("")
    (inner / "models.py").write_text(
        "from crawley.persistance import Entity, Field, Unicode\n"
        "class CmdAuthor(Entity):\n"
        "    title = Field(Unicode(255))\n"
    )
    (inner / "crawlers.py").write_text(
        "from crawley.crawlers import BaseCrawler\n"
        "from crawley.scrapers import BaseScraper\n"
        "from models import CmdAuthor\n"
        "class S(BaseScraper):\n"
        "    matching_urls = ['%/page%']\n"
        "    def scrape(self, response):\n"
        "        CmdAuthor(title=response.html.xpath('//h1')[0].text)\n"
        "class C(BaseCrawler):\n"
        "    start_urls = [" + repr(server + "/") + "]\n"
        "    scrapers = [S]\n"
        "    max_depth = 1\n"
        "    requests_delay = 0\n"
        "    requests_deviation = 0\n"
    )

    add_to_path(str(project))
    importlib.invalidate_caches()
    settings = importlib.import_module("settings")

    # Reset the crawler registry so only this project's crawler runs.
    from crawley.crawlers import base as crawler_base

    crawler_base.user_crawlers.clear()

    from crawley.manager.commands.run import RunCommand

    RunCommand(settings=settings).checked_execute()

    sqlite_file = db_path + ".sqlite"
    assert os.path.exists(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    titles = [row[0] for row in conn.execute("select title from cmdauthor")]
    conn.close()
    assert any("Title" in t for t in titles)
