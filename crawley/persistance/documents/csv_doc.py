"""CSV document storage."""

import csv

from crawley.persistance.documents.meta import BaseDocument, BaseDocumentSession

csv_objects = []


class CSVDocument(BaseDocument):
    """A row to be dumped as CSV."""

    def __init__(self, **kwargs):
        csv_objects.append(kwargs)


class Session(BaseDocumentSession):
    """Dump the scraped rows to a CSV file."""

    def commit(self):
        if not csv_objects:
            open(self.file_name, "w", encoding="utf-8").close()
            return

        fieldnames = list(csv_objects[0].keys())
        with open(self.file_name, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_objects:
                writer.writerow(row)


csv_session = Session()
