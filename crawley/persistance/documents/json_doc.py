"""JSON document storage."""

import json

from crawley.persistance.documents.meta import BaseDocument, BaseDocumentSession

json_objects = []


class JSONDocument(BaseDocument):
    """A row to be dumped as JSON."""

    def __init__(self, **kwargs):
        json_objects.append(kwargs)


class Session(BaseDocumentSession):
    """Dump the scraped rows to a JSON file."""

    def commit(self):
        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(json_objects, f, ensure_ascii=False, indent=2)


json_session = Session()
