import pytest

from periskop_client.collector import ExceptionCollector
from periskop_client.exporter import ExceptionExporter
from periskop_client.models import HTTPContext


@pytest.fixture
def collector():
    return ExceptionCollector()


@pytest.fixture
def exporter(collector):
    return ExceptionExporter(collector)


@pytest.fixture
def sample_http_context():
    return HTTPContext(request_method="GET", request_url="http://example.com",
                       request_headers={"Cache-Control": "no-cache"})

@pytest.fixture
def sample_http_context_with_request_body():
    return HTTPContext(request_method="GET", request_url="http://example.com",
                       request_headers={"Cache-Control": "no-cache"},
                       request_body="some body")

def get_exception_with_context(collector):
    return list(collector._aggregated_exceptions.values())[0].latest_errors[0]
