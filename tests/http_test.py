import unittest
import threading
import SocketServer

from crawley.http.request import Request
from tests.http_daemon import ServerHandler


class RequestTest(unittest.TestCase):
    '''
    This is a unittest for the Request class, the main reason for writing this
    unittest was the migration to the "requests" library:

        https://github.com/kennethreitz/grequests/

    @author: Andres Riancho <andres . riancho | gmail . com>
    '''
    IP_ADDRESS = "127.0.0.1"
    PORT = 8011

    def setUp(self):
        for port in xrange(self.PORT, self.PORT + 50):
            try:
                self.httpd = SocketServer.TCPServer((self.IP_ADDRESS,
                                                     port),
                                                    ServerHandler)
            except:
                pass
            else:
                self.PORT = port
                break

        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.RequestHandlerClass.requests = []

    def test_simple_GET(self):
        r = Request('http://%s:%s/hello' % (self.IP_ADDRESS, self.PORT))
        response_body = r.get_response().text

        self.assertEqual(response_body, 'ABCDEF\n')
        self.assertEqual(len(self.httpd.RequestHandlerClass.requests), 1)

        request = self.httpd.RequestHandlerClass.requests[0]
        self.assertEqual(request.path, '/hello')
        self.assertEqual(request.command, 'GET')
        self.assertEqual(request.request_version, 'HTTP/1.1')
        self.assertIn('host', request.headers)
        self.assertEqual(request.request_body, None)

    def test_GET_cookie(self):
        r = Request('http://%s:%s/hello' % (self.IP_ADDRESS, self.PORT))
        r.get_response()

        r.url = 'http://%s:%s/world' % (self.IP_ADDRESS, self.PORT)
        response = r.get_response()

        self.assertEqual(response.text, 'ABCDEF\n')
        self.assertEqual(len(self.httpd.RequestHandlerClass.requests), 2)

        request = self.httpd.RequestHandlerClass.requests[0]
        self.assertEqual(request.path, '/hello')
        self.assertEqual(request.command, 'GET')
        self.assertEqual(request.request_version, 'HTTP/1.1')
        self.assertIn('host', request.headers)
        self.assertEqual(request.request_body, None)

        request = self.httpd.RequestHandlerClass.requests[1]
        self.assertEqual(request.path, '/world')
        self.assertEqual(request.command, 'GET')
        self.assertEqual(request.request_version, 'HTTP/1.1')
        self.assertIn('cookie', request.headers)
        self.assertEqual(request.headers['cookie'], 'cookie=123456')
        self.assertEqual(request.request_body, None)

