"""Persistence layer.

Re-exports the relational entities/fields, the document storages and the
NoSQL entities so user models can simply do::

    from crawley.persistance import Entity, UrlEntity, Field, Unicode
"""

from crawley.persistance.documents import (
    CSVDocument,
    JSONDocument,
    XMLDocument,
    csv_session,
    json_session,
    xml_session,
)
from crawley.persistance.nosql import CouchEntity, MongoEntity
from crawley.persistance.relational.databases import (
    Entity,
    Field,
    Unicode,
    UnicodeText,
    UrlEntity,
    session,
    setup,
)

__all__ = [
    "Entity",
    "UrlEntity",
    "Field",
    "Unicode",
    "UnicodeText",
    "session",
    "setup",
    "JSONDocument",
    "XMLDocument",
    "CSVDocument",
    "json_session",
    "xml_session",
    "csv_session",
    "MongoEntity",
    "CouchEntity",
]
