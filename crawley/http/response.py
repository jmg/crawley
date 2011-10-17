"""
    HTTP crawley's response object
"""

class Response(object):
    """
        Class that encapsulates an HTTP response
    """

    def __init__(self, rawHtml, html, url):

        self.raw_html = rawHtml
        self.url = url
        self.html = html
