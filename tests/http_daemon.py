import SimpleHTTPServer
import SocketServer

PORT = 8000

class LoggedRequest(object):
    def __init__(self, command, path, request_version, headers, request_body):
        self.command = command
        self.path = path
        self.request_version = request_version
        self.headers = dict(headers)
        self.request_body = request_body

    def __repr__(self):
        return '<LoggedRequest %s %s %s>' % (self.command, self.path,
                                             self.request_version)

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    requests = []

    def do_GET(self):
        """Serve a GET request."""
        self.send_response(200)
        self.send_header("Set-Cookie", 'cookie=123456')
        self.end_headers()

        self.wfile.write('ABCDEF\n')

    def handle_one_request(self):
        # TODO: Add support for reading self.rfile
        request_body = None

        SimpleHTTPServer.SimpleHTTPRequestHandler.handle_one_request(self)
        self.requests.append(LoggedRequest(self.command, self.path,
                                           self.request_version, self.headers,
                                           request_body))


if __name__ == '__main__':
    httpd = SocketServer.TCPServer(("127.0.0.1", PORT), ServerHandler)

    print "Serving at port", PORT
    httpd.serve_forever()
