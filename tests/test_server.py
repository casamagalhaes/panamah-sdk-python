import multiprocessing
import os
import re
import shutil
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from .test_routes import routes

#https://gist.github.com/tliron/8e9757180506f25e46d9
class TestHTTPServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.routes = routes
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def do_HEAD(self):
        self.handle_method('HEAD')

    def do_GET(self):
        self.handle_method('GET')

    def do_POST(self):
        self.handle_method('POST')

    def do_PUT(self):
        self.handle_method('PUT')

    def do_DELETE(self):
        self.handle_method('DELETE')

    def get_route(self):
        for path, route in self.routes.items():
            if re.match(path, self.path):
                return route
        return None

    def get_payload(self):
        payload_len = int(self.headers.getheader('content-length', 0))
        payload = self.rfile.read(payload_len)
        payload = json.loads(payload)
        return payload

    def handle_method(self, method):
        route = self.get_route()
        if route is None:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(bytes('Route not found\n', 'utf-8'))
        else:
            if method == 'HEAD':
                self.send_response(200)
                if 'media_type' in route:
                    self.send_header('Content-type', route['media_type'])
                self.end_headers()
            else:
                if 'file' in route:
                    if method == 'GET':
                        try:
                            f = open(os.path.join(here, route['file']))
                            try:
                                self.send_response(200)
                                if 'media_type' in route:
                                    self.send_header(
                                        'Content-type', route['media_type'])
                                self.end_headers()
                                shutil.copyfileobj(f, self.wfile)
                            finally:
                                f.close()
                        except:
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write(
                                bytes('File not found\n', 'utf-8')
                            )
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write(
                            bytes('Only GET is supported\n', 'utf-8')
                        )
                else:
                    if method in route:
                        content = route[method](self)
                        if content is not None:
                            self.send_response(200)
                            if 'media_type' in route:
                                self.send_header(
                                    'Content-type', route['media_type'])
                            self.end_headers()
                            if method != 'DELETE':
                                self.wfile.write(
                                    bytes(json.dumps(content), 'utf-8'))
                        else:
                            self.send_response(404)
                            self.end_headers()
                            self.wfile.write(bytes('Not found\n', 'utf-8'))
                    else:
                        self.send_response(405)
                        self.end_headers()
                        self.wfile.write(
                            bytes(method + ' is not supported\n', 'utf-8'))


def start_server():
    server_address = ('127.0.0.1', 2020)
    print('Starting server -> %s:%d' % server_address)
    httpd = HTTPServer(server_address, TestHTTPServer)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


_process = None


def start():
    _process = multiprocessing.Process(target=start_server, args=())
    _process.daemon = True
    _process.start()


def stop():
    if not _process is None:
        _process.stop()
