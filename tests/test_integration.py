import threading
import requests
from http.server import HTTPServer


from periskop.handler import exception_http_handler
from periskop.models import HTTPContext


def err_func():
    return 1 / 0


def test_integration(collector, exporter):
    try:
        err_func()
    except Exception as exception:
        collector.report(exception)
        collector.report_with_context(exception,
                                      HTTPContext("GET", "http://example.com", {"Cache-Control": "no-cache"}))
    server_address = ('', 8686)
    httpd = HTTPServer(server_address, exception_http_handler(path="/-/exceptions", exporter=exporter))
    t = threading.Thread(target=httpd.serve_forever)
    t.daemon = True
    t.start()
    response = requests.get("http://localhost:8686/-/exceptions")
    assert response.status_code == 200
    assert response.json()['aggregated_errors'][0]['total_count'] == 2
