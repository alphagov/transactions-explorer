from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import re
import threading
import time

PATH_TO_STATIC_FILES = "../../output"


def rewrite_request(path):
    new_path = path
    if not re.match(r'.*\..*$', path):
        new_path += '.html'

    return new_path


class HttpStub(BaseHTTPRequestHandler):

    thread = None
    server = None

    def do_GET(self):
        # rewrite requests to point at flat *.html files
        print self.path, "<--------------- \n"
        path_to_html = rewrite_request(self.path)
        print path_to_html
        with open(PATH_TO_STATIC_FILES + path_to_html, mode='r') as f:
            self.send_response(200)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            self.wfile.write(f.read())

        return

    @classmethod
    def start(cls):
        cls.server = HTTPServer(("", 8000), cls)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.start()

    @classmethod
    def stop(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

if __name__ == "__main__":
    HttpStub.start()
