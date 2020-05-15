import traceback
from typing import Dict

from .models import (
    AggregatedException,
    ExceptionInstance,
    ExceptionWithContext,
    HTTPContext,
    Payload,
)


class ExceptionCollector:
    def __init__(self):
        self._aggregated_exceptions: Dict[str, AggregatedException] = {}

    def report(self, exception: Exception):
        """
        Report an exception

        :param Exception exception: captured exception
        """
        self._add_exception(exception)

    def report_with_context(self, exception: Exception, http_context: HTTPContext):
        """
        Report an exception with the context of an HTTP request

        :param Exception exception: captured exception
        :param HTTPContext http_context: context of an HTTP request
        """
        self._add_exception(exception, http_context)

    def get_aggregated_exceptions(self) -> Payload:
        """
        Get all aggregated exceptions in a list format

        :return Payload: list of aggregated exceptions
        """
        return Payload(aggregated_errors=list(self._aggregated_exceptions.values()))

    def _add_exception(self, exception: Exception, http_context: HTTPContext = None):
        stacktrace = traceback.format_exc().strip().split("\n")
        error_class = type(exception).__name__

        exception_instance = ExceptionInstance(
            cls=error_class, message=str(exception), stacktrace=stacktrace
        )
        exception_with_context = ExceptionWithContext(
            error=exception_instance, http_context=http_context
        )

        aggregation_key = exception_with_context.aggregation_key()
        if aggregation_key not in self._aggregated_exceptions:
            self._aggregated_exceptions[aggregation_key] = AggregatedException(
                aggregation_key=aggregation_key, latest_errors=[]
            )
        self._aggregated_exceptions[aggregation_key].add_exception(
            exception_with_context
        )
