"""
    HTTP crawley's response object
"""

class Response(object):
    """
        Class that encapsulates an HTTP response
    """

    def __init__(self, html, url):

        self.html = html
        self.url = url
