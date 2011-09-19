"""
    Data Extractors classes
"""

import pyquery

from lxml import etree
from StringIO import StringIO


class PyQueryExtractor(object):
    """
        Extractor using PyQuery (A JQuery-like library for Python)
    """
    
    def get_object(self, data):
        
        html = pyquery(data)
        return html
        

class XPathExtractor(object):
    """
        Extractor using Xpath
    """
    
    def get_object(self, data):  
              
        parser = etree.HTMLParser()
        html = etree.parse(StringIO(data), parser)
        return html
