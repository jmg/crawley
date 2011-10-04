import unittest
import os
from crawley.persistance.documents import XMLDocument, session

class TestDoc(XMLDocument):
    
    pass


class PersistanceTest(unittest.TestCase):
    
    def setUp(self):
        
        pass
    
    def test_XMLDocument(self):
        
        doc = TestDoc(attribute="test_value")
        doc = TestDoc(attribute="test_value2")
        session.commit()
        
        self.assertTrue(os.path.exists("data.xml"))
        os.remove("data.xml")
