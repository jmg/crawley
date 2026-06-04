"""NoSQL storages (MongoDB, CouchDB)."""

from crawley.persistance.nosql.couch import CouchEntity, couch_session
from crawley.persistance.nosql.mongo import MongoEntity, mongo_session

__all__ = ["MongoEntity", "mongo_session", "CouchEntity", "couch_session"]
