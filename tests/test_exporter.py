import json
from unittest import mock
from freezegun import freeze_time


@freeze_time("2019-10-11 12:47:25.595")
def test_export(collector, exporter, sample_http_context):
    expected = """
{
	"target_uuid": "5d9893c6-51d6-11ea-8aad-f894c260afe5",
  "aggregated_errors": [
    {
      "aggregation_key": "Exception@a9a59d26",
      "total_count": 1,
      "severity": "error",
      "created_at": "2019-10-11T12:47:25.595Z",
      "latest_errors": [
        {
          "error": {
            "class": "Exception",
            "message": "test",
            "stacktrace": ["NoneType: None"],
            "cause": null
          },
          "uuid": "5d9893c6-51d6-11ea-8aad-f894c260afe5",
          "timestamp": "2019-10-11T12:47:25.595Z",
          "severity": "error",
          "http_context": {
            "request_method": "GET",
            "request_url": "http://example.com",
            "request_headers": {
              "Cache-Control": "no-cache"
            },
            "request_body": null
          }
        }
      ]
    }
  ]
}"""
    with mock.patch("uuid.uuid1", return_value="5d9893c6-51d6-11ea-8aad-f894c260afe5"):
        collector.report_with_context(exception=Exception("test"), http_context=sample_http_context)
        collector._uuid = "5d9893c6-51d6-11ea-8aad-f894c260afe5"
        exported = exporter.export()
        assert json.loads(exported) == json.loads(expected)
