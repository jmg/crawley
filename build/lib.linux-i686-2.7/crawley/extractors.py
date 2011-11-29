"""
    Data Extractors classes
"""

from pyquery import PyQuery

from lxml import etree
from StringIO import StringIO


class PyQueryExtractor(object):
    """
        Extractor using PyQuery (A JQuery-like library for Python)
    """
    
    def get_object(self, data):
        
        html = PyQuery(data)
        return html
        

class XPathExtractor(object):
    """
        Extractor using Xpath
    """
    
    def get_object(self, data):  
              
        parser = etree.HTMLParser()
        html = etree.parse(StringIO(data), parser)
        return html


class RawExtractor(object):
    """
        Returns the raw html data
        Use your favourite python tool to scrape it.        
    """
    
    def get_object(self, data):
        
        return data
