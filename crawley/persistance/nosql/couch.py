"""CouchDB storage.

The legacy ``couchdb`` package is unmaintained on Python 3, so this uses a
tiny ``httpx`` based client talking to CouchDB's HTTP API directly.
"""

import logging

from crawley.persistance.nosql.base import BaseNosqlSession, NosqlEntity

log = logging.getLogger("crawley.persistance.couch")

couch_objects = []


class CouchEntity(NosqlEntity):
    collection = couch_objects


class Session(BaseNosqlSession):
    def set_up(self, settings, storage_name):
        super().set_up(settings, storage_name)

        import httpx

        self.db_name = settings.COUCH_DB_NAME
        self.client = httpx.Client(base_url=self.db_host.rstrip("/"))

        # Create the database if it does not exist yet (idempotent).
        self.client.put("/%s" % self.db_name)

    def commit(self):
        for _entity, obj in couch_objects:
            if getattr(self.settings, "SHOW_DEBUG_INFO", False):
                log.debug("%s", obj)
            self.client.post("/%s" % self.db_name, json=dict(obj))

    def close(self):
        if hasattr(self, "client"):
            self.client.close()


couch_session = Session()
