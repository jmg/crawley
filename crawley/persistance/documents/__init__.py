"""Document storages (JSON, XML, CSV)."""

from crawley.persistance.documents.csv_doc import CSVDocument, csv_session
from crawley.persistance.documents.json_doc import JSONDocument, json_session
from crawley.persistance.documents.meta import documents_entities
from crawley.persistance.documents.xml import XMLDocument, xml_session

__all__ = [
    "JSONDocument",
    "json_session",
    "XMLDocument",
    "xml_session",
    "CSVDocument",
    "csv_session",
    "documents_entities",
]
