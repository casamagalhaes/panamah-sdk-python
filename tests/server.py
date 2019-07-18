import multiprocessing
import os
import re
import shutil
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from .routes import routes
import requests

next_payload = None
next_status_code = -1


'''
Based on the implementation of @tliron
https://gist.github.com/tliron/8e9757180506f25e46d9

'''
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
        payload_len = int(self.headers['content-length'])
        payload = self.rfile.read(payload_len)
        print(payload)
        payload = json.loads(payload)
        return payload

    def check_for_next_response(self):
        global next_status_code
        global next_payload
        if self.path == '/set-response':
            payload = self.get_payload()
            next_status_code = payload['status_code']
            next_payload = payload['payload']
            self.send_response(200)
            self.end_headers()
            return True
        elif self.path == '/clear-response':
            next_status_code = -1
            next_payload = None
            self.send_response(200)
            self.end_headers()
            return True
        return False

    def handle_method(self, method):
        global next_status_code
        global next_payload
        if self.check_for_next_response():
            return
        elif (next_status_code > -1) and (not next_payload is None):
            self.send_response(next_status_code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(next_payload), 'utf-8'))
        else:
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


server_address = ('127.0.0.1', 2020)


def start_server():
    print('Starting server -> %s:%d' % server_address)
    httpd = HTTPServer(server_address, TestHTTPServer)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


def set_next_response(status_code, payload):
    try:
        response = requests.post(
            url='http://%s:%d/set-response' % server_address,
            json={'status_code': status_code, 'payload': payload}
        )
        return response.status_code == 200
    except:
        pass


def clear_next_response():
    try:
        response = requests.post(
            url='http://%s:%d/clear-response' % server_address
        )
        return response.status_code == 200
    except:
        pass


_process = None


def start():
    _process = multiprocessing.Process(target=start_server, args=())
    _process.daemon = True
    _process.start()


def stop():
    if not _process is None:
        _process.stop()
