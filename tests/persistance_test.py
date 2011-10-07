import unittest
import os
from crawley.persistance.documents import XMLDocument, JSONDocument, json_session, xml_session

class TestXMLDoc(XMLDocument):
    pass

class TestJSONDoc(JSONDocument):
    pass

class PersistanceTest(unittest.TestCase):
    
    def setUp(self):
        
        pass
    
    def test_XMLDocument(self):
        
        doc = TestXMLDoc(attribute="test_value")
        doc = TestXMLDoc(attribute="test_value2")
        xml_session.commit()
        
        self.assertTrue(os.path.exists("data.xml"))
        os.remove("data.xml")

    def test_JSONDocument(self):
    
        doc = TestJSONDoc(attribute="test_value")
        doc = TestJSONDoc(attribute="test_value2")
        json_session.commit()
        
        self.assertTrue(os.path.exists("data.json"))
        os.remove("data.json")
