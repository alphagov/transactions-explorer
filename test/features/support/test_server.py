from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import os
import re
import socket
import threading
import time
from urlparse import urlparse
import errno
import requests
import signal
import sys


HTML_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'output'))

SPEC_ROOT= os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         '..', '..', '..', 'spec'))

def has_extension(path):
    return bool(os.path.splitext(path)[1])


def find_file_to_serve(path):
    url = urlparse(path)

    if url.query:
        path = url.path

    if any(substring in path.lower() for substring in ('spec', 'jasmine')):
        abs_path = os.path.join(SPEC_ROOT, path.lstrip('/'))
    else:
        abs_path = os.path.join(HTML_ROOT, path.lstrip('/'))

    if os.path.isdir(abs_path):
        abs_path = os.path.join(abs_path, 'index.html')

    if not has_extension(abs_path):
        abs_path += '.html'

    return abs_path if os.path.isfile(abs_path) else None


def wait_until(condition, timeout=15, interval=0.1):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if condition():
            return
        time.sleep(interval)
    raise RuntimeError("timeout: condition not met in wait_until")


def get_content_type(full_path):
    return mimetypes.guess_type(full_path)[0]


def _is_broken_pipe(socket_error):
    return (isinstance(socket_error.args, tuple)
            and socket_error[0] == errno.EPIPE)


class TestServer(BaseHTTPRequestHandler):

    thread = None
    server = None

    def __alive(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("stub server is running")
        return

    def __serve_file(self):
        file_path = find_file_to_serve(self.path)

        if not file_path:
            self.send_response(404)
        
        else:
            with open(file_path, mode='r') as file:
                self.send_response(200)

                self.send_header("Content-type", get_content_type(file_path))
                self.end_headers()
                self.wfile.write(file.read())

        return

    def do_GET(self):
        try:
            if self.path == "/__alive__":
                self.__alive()
            else:
                self.__serve_file()
        except socket.error as e:
            if _is_broken_pipe(e):
                # client closed connection - ignore it
                pass
            else:
                raise e

    def log_request(self, code='-', size='-'):
        pass

    @classmethod
    def start(cls, port=8000):
        cls.server = HTTPServer(("", port), cls)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()
        wait_until(cls._running)

    @classmethod
    def stop(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    @classmethod
    def _running(cls):
        try:
            alive = 'http://localhost:%d/__alive__' % cls.server.server_port
            return requests.get(alive).status_code == 200
        except:
            print "error waiting for server to start"
            return False

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    TestServer.start(port=port)
    print "Running on port %d" % port

    def stop(signal, frame):
        TestServer.stop()
        print "\nBye"

    signal.signal(signal.SIGINT, stop)
    signal.pause()
