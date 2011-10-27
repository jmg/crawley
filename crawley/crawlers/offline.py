from base import BaseCrawler
from lxml import etree
from crawley.extractors import XPathExtractor
from StringIO import StringIO

class OffLineCrawler(BaseCrawler):
    
    def __init__(self, *args, **kwargs):
        
        BaseCrawler.__init__(self, *args, **kwargs)
        
    def _get_response(self, url, data=None):
        
        response = BaseCrawler._get_response(self, url, data)
               
        fixer = HTMLFixer(self._url_regex, url, response.raw_html)        
        html = fixer.get_fixed_html()
        
        return html
                

class HTMLFixer(object):
        
    def __init__(self, url_regex, url, html):
        
        self._url_regex = url_regex
        self.url = url
        self.html_tree = XPathExtractor().get_object(html)
    
    def get_fixed_html(self):
            
        self._fix_tags("link", "href")
        self._fix_tags("img", "src")
        
        return etree.tostring(self.html_tree.getroot(), pretty_print=True, method="html")
        
    def _fix_tags(self, tag, attrib):
        
        tags = self.html_tree.xpath("//%s" % tag)
        
        for tag in tags:
            if not self._url_regex.match(tag.attrib[attrib]):
                tag.attrib[attrib] = "%s/%s" % (self.url, tag.attrib[attrib])
