from elixir import entities
from eventlet import GreenPool

from crawley.crawlers import user_crawlers, BaseCrawler, FastCrawler
from crawley.persistance import Entity, UrlEntity, setup

from command import ProjectCommand
from syncdb import SyncDbCommand
from utils import import_user_module


class RunCommand(ProjectCommand):
    """
        Run the user's crawler

        Reads the crawlers.py file to obtain the user's crawler classes
        and then run these crawlers.
    """

    name = "run"

    def execute(self):
        
        syncdb = SyncDbCommand(args=self.args, settings=self.settings)
        syncdb.checked_execute()
        sessions = syncdb.sessions

        crawler = import_user_module("crawlers")
        models = import_user_module("models")
        
        url_storage = None
                
        for entity in entities:
            if isinstance(entity, UrlEntity):
                url_storage = entity
        
        pool = GreenPool()
        
        crawlers = [c for c in user_crawlers if not c is BaseCrawler and c is not FastCrawler]
                
        for crawler_class in crawlers:

            spider = crawler_class(storage=url_storage, sessions=sessions, debug=self.settings.SHOW_DEBUG_INFO)
            pool.spawn_n(spider.start)

        pool.waitall()
