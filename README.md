# periskop-python
[![pypi](https://img.shields.io/pypi/v/periskop-client.svg)](https://pypi.python.org/pypi/periskop-client/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/periskop-client.svg)](https://pypi.python.org/pypi/periskop-client/) [![Build Status](https://api.cirrus-ci.com/github/soundcloud/periskop-python.svg)](https://cirrus-ci.com/github/soundcloud/periskop-python)


[Periskop](https://github.com/soundcloud/periskop) requires collecting and aggregating exceptions on the client side,
as well as exposing them via an HTTP endpoint using a well defined format.

This library provides low level collection and rendering capabilities

## Install

```
pip install periskop-client
```

## Usage example

```python
import json
from http.server import HTTPServer

from periskop_client.collector import ExceptionCollector
from periskop_client.exporter import ExceptionExporter
from periskop_client.handler import exception_http_handler
from periskop_client.models import HTTPContext


def faulty_json():
    return json.loads('{"id":')


if __name__ == "__main__":
    collector = ExceptionCollector()
    try:
        faulty_json()
    except Exception as exception:
        # Report without context
        collector.report(exception)
        # Report with HTTP context without request body
        collector.report_with_context(
            exception,
            HTTPContext("GET", "http://example.com", {"Cache-Control": "no-cache"}),
        )
        # Report with HTTP context with request body
        collector.report_with_context(
            exception,
            HTTPContext("GET", "http://example.com", {"Cache-Control": "no-cache"}, "request_body"),
        )

    # Expose collected exceptions in localhost:8081/-/exceptions
    server_address = ("", 8081)
    handler = exception_http_handler(
        path="/-/exceptions", exporter=ExceptionExporter(collector)
    )
    http_server = HTTPServer(server_address, handler)
    http_server.serve_forever()
```

### Using push gateway

You can also use [pushgateway](https://github.com/soundcloud/periskop-pushgateway) in case you want to push your metrics 
instead of using pull method. Use only in case you really need it (e.g a batch job) as it would degrade the performance 
of your application. In the following example, we assume that we deployed an instance of periskop-pushgateway 
on `http://localhost:6767`:

```scala
exporter = ExceptionExporter(collector)
exporter.push_to_gateway("http://localhost:6767")
```

## Run tests

For running tests [pytest](https://docs.pytest.org) is needed. A recommended way to run all check is installing [tox](https://tox.readthedocs.io/en/latest/install.html) and then just type `tox`. This will run `pytest` tests, [black](https://black.readthedocs.io) formatter and [flake8](https://flake8.pycqa.org) and [mypy](http://mypy-lang.org/) static code analyzers.

Alternatively you can run `pip install -r requirements-tests.txt` and then run `pytest`.
