import unittest
import os
from crawley.persistance.documents import XMLDocument, JSONDocument, CSVDocument, json_session, xml_session, csv_session

class TestXMLDoc(XMLDocument):
    pass

class TestJSONDoc(JSONDocument):
    pass

class TestCSVDoc(CSVDocument):
    pass

class PersistanceTest(unittest.TestCase):

    def setUp(self):

        pass

    def test_XMLDocument(self):

        doc = TestXMLDoc(attribute="test_value")
        doc = TestXMLDoc(attribute="test_value2")
        xml_session.file_name = "data.xml"
        xml_session.commit()

        self.assertTrue(os.path.exists("data.xml"))
        os.remove("data.xml")

    def test_JSONDocument(self):

        doc = TestJSONDoc(attribute="test_value")
        doc = TestJSONDoc(attribute="test_value2")
        json_session.file_name = "data.json"
        json_session.commit()

        self.assertTrue(os.path.exists("data.json"))
        os.remove("data.json")

    def test_CVSDocument(self):

        doc = TestCSVDoc(attribute="test_value")
        doc = TestCSVDoc(attribute="test_value2")
        csv_session.file_name = "data.csv"
        csv_session.commit()

        self.assertTrue(os.path.exists("data.csv"))
        os.remove("data.csv")
