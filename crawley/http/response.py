"""
    HTTP crawley's response object
"""

class Response(object):
    """
        Class that encapsulates an HTTP response
    """

    def __init__(self, raw_html=None, extracted_html=None, url=None, response=None):

        self.raw_html = raw_html
        self.html = extracted_html
        self.url = url        
        
        if response is not None:
            self.headers = response.headers
            self.code = response.getcode()
