"""Serve the frontend and proxy /api to the existing Flask backend (same origin)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def _proxy(self):
        url = 'http://127.0.0.1:5000' + self.path
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length) if length else None
        headers = {k: v for k, v in self.headers.items() if k.lower() in ('authorization', 'content-type')}
        req = Request(url, data=body, headers=headers, method=self.command)
        try:
            with urlopen(req, timeout=15) as response:
                self._send_proxy(response.status, response.read(), response.headers.get('Content-Type', 'application/json'))
        except HTTPError as e:
            self._send_proxy(e.code, e.read(), e.headers.get('Content-Type', 'application/json'))
        except (URLError, TimeoutError):
            self._send_proxy(502, b'{"error":"No se pudo conectar con Flask en el puerto 5000"}', 'application/json')

    def _send_proxy(self, status, body, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith('/api/'):
            return self._proxy()
        return super().do_GET()

    def do_POST(self):
        return self._proxy() if self.path.startswith('/api/') else self.send_error(404)

    def do_PATCH(self):
        return self._proxy() if self.path.startswith('/api/') else self.send_error(404)

    def do_PUT(self):
        return self._proxy() if self.path.startswith('/api/') else self.send_error(404)

    def do_DELETE(self):
        return self._proxy() if self.path.startswith('/api/') else self.send_error(404)

if __name__ == '__main__':
    print('Frontend: http://127.0.0.1:8000')
    print('API proxy: http://127.0.0.1:5000/api')
    ThreadingHTTPServer(('127.0.0.1', 8000), Handler).serve_forever()
