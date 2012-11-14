"""
    HTTP crawley's response object
"""

class Response(object):
    """
        Class that encapsulates an HTTP response
    """

    def __init__(self, raw_html=None, binary_content=None, extracted_html=None, url=None, response=None):

        self.raw_html = raw_html
        self.html = extracted_html
        self.url = url
        self.binary_content = binary_content
        self.response = response

        if response is not None:
            self.headers = response.headers
            self.code = response.status_code
