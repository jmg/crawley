"""XML document storage."""

from lxml import etree

from crawley.persistance.documents.meta import BaseDocument, BaseDocumentSession

root = etree.Element("root")


class XMLDocument(BaseDocument):
    """A row to be dumped as XML."""

    def __init__(self, **kwargs):
        row = etree.SubElement(root, self.__class__.__name__)
        for key, value in kwargs.items():
            element = etree.SubElement(row, key)
            element.text = "" if value is None else str(value)


class Session(BaseDocumentSession):
    """Dump the scraped rows to an XML file."""

    def commit(self):
        with open(self.file_name, "wb") as f:
            f.write(
                etree.tostring(
                    root,
                    pretty_print=True,
                    xml_declaration=True,
                    encoding="UTF-8",
                )
            )


xml_session = Session()
