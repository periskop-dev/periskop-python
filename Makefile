clean:
	rm -rf .mypy_cache .tox __pycache__

test:
	pip install -r requirements-tests.txt
	pytest

auto-format:
	black periskop_client

.PHONY: clean test auto-format