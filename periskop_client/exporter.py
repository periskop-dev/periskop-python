from .collector import ExceptionCollector


class ExceptionExporter:
    def __init__(self, collector: ExceptionCollector):
        self._collector = collector

    def export(self) -> str:
        """
        Export the collection of errors in JSON format

        :return: str
        """
        return self._collector.get_aggregated_exceptions().to_json()  # type: ignore
