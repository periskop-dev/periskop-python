from .conftest import get_exception_with_context


def test_add_exception(collector):
    exception = Exception()
    collector._add_exception(exception, None)
    assert len(collector._aggregated_exceptions) == 1
    collector._add_exception(exception, None)
    assert list(collector._aggregated_exceptions.values())[0].total_count == 2


def test_report(collector):
    collector.report(Exception("error"))
    assert len(collector._aggregated_exceptions) == 1
    exception_with_context = get_exception_with_context(collector)
    assert exception_with_context.error.cls == "Exception"
    assert exception_with_context.error.message == "error"
    assert len(exception_with_context.error.stacktrace) != 0


def test_report_with_context(collector, sample_http_context):
    collector.report_with_context(Exception("error"), sample_http_context)
    assert len(collector._aggregated_exceptions) == 1
    exception_with_context = get_exception_with_context(collector)
    assert exception_with_context.http_context.request_method == "GET"


def test_get_aggregated_exceptions(collector):
    collector._add_exception(Exception(), None)
    payload = collector.get_aggregated_exceptions()
    aggregated_error = list(collector._aggregated_exceptions.values())[0]
    assert payload.aggregated_errors[0].aggregation_key == aggregated_error.aggregation_key
