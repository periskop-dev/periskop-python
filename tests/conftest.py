import pytest

from periskop.collector import ExceptionCollector
from periskop.exporter import ExceptionExporter
from periskop.models import HTTPContext


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


def get_exception_with_context(collector):
    return list(collector._aggregated_exceptions.values())[0].latest_errors[0]
