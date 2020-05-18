from http.server import BaseHTTPRequestHandler

from .exporter import ExceptionExporter


def exception_http_handler(path: str, exporter: ExceptionExporter):
    """
    Factory function to create an HTTP Handler wraped with a Periskop exporter.

    :param str path: path to server exported exceptions
    :param ExceptionExporter exporter: exporter object to use as expose a JSON

    :return ExceptionBaseHTTPRequestHandler:
    """

    class ExceptionBaseHTTPRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            self._exporter = exporter
            super().__init__(*args, **kwargs)

        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

        def do_GET(self):
            if self.path == path:
                self._set_headers()
                self.wfile.write(self._exporter.export().encode(encoding="utf_8"))

    return ExceptionBaseHTTPRequestHandler
