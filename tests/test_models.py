import pytest

from periskop.models import ExceptionWithContext, ExceptionInstance, AggregatedException, MAX_ERRORS


def _mock_exception_with_context(stacktrace):
    exception_instance = ExceptionInstance(cls="IndexError", message="Out of range", stacktrace=stacktrace)
    return ExceptionWithContext(error=exception_instance, http_context=None)


@pytest.mark.parametrize("expected_key,stacktrace", [
    ("IndexError@d41d8cd9", [""]),
    ("IndexError@0f793ec8", ["line 0:", "division by zero"]),
    ("IndexError@b4c6d908", ["line 0:", "division by zero", "error", "line 1:", "my_func()", "a"]),
    ("IndexError@b4c6d908", ["line 0:", "division by zero", "error", "line 1:", "my_func()", "b"]),
])
def test_exception_with_context_aggregation_key(expected_key, stacktrace):
    exception_with_context = _mock_exception_with_context(stacktrace)
    assert exception_with_context.aggregation_key() == expected_key


def test_aggregated_exception_add_exception():
    exception_with_context = _mock_exception_with_context([""])
    aggregated_exception = AggregatedException(aggregation_key="error@hash", latest_errors=[])
    aggregated_exception.add_exception(exception_with_context)
    assert aggregated_exception.total_count == 1
    for _ in range(MAX_ERRORS):
        aggregated_exception.add_exception(exception_with_context)
    assert aggregated_exception.total_count == MAX_ERRORS + 1
    assert len(aggregated_exception.latest_errors) == MAX_ERRORS
