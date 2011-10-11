from elixir import entities
from eventlet import GreenPool

from crawley.crawlers import user_crawlers
from crawley.persistance import UrlEntity

from command import ProjectCommand
from syncdb import SyncDbCommand
from crawley.manager.utils import import_user_module, search_class


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

        crawler = import_user_module("crawlers")
        models = import_user_module("models")
                
        url_storage = search_class(UrlEntity, entities)
        
        pool = GreenPool()                
                
        for crawler_class in user_crawlers:

            spider = crawler_class(storage=url_storage, sessions=syncdb.sessions, debug=self.settings.SHOW_DEBUG_INFO)
            pool.spawn_n(spider.start)

        pool.waitall()
