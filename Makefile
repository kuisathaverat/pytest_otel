# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

OTEL_EXPORTER_OTLP_ENDPOINT ?= http://127.0.0.1:4317
OTEL_SERVICE_NAME ?= "pytest_otel_test"
OTEL_EXPORTER_OTLP_INSECURE ?= True
OTEL_EXPORTER_OTLP_HEADERS ?=
TRACEPARENT ?=
DEMO_DIR ?= docs/demos

VENV ?= .venv
PYTHON ?= python3
PIP ?= pip3

SHELL = /bin/bash
.SILENT:

.PHONY: help
help:
	@echo "Targets:"
	@echo ""
	@grep '^## @help' Makefile|cut -d ":" -f 2-3|( (sort|column -s ":" -t) || (sort|tr ":" "\t") || (tr ":" "\t"))

## @help:virtualenv:Create a Python virtual environment.
.PHONY: virtualenv
virtualenv:
	$(PYTHON) --version
	test -d $(VENV) || $(PYTHON) -m venv $(VENV);\
	source $(VENV)/bin/activate; \
	$(PIP) install ".[test]";

## @help:test:Run the test.
.PHONY: test
test: virtualenv
	source $(VENV)/bin/activate;\
	$(PYTHON) -m pytest --capture=no -p pytester --runpytest=subprocess \
		--junitxml $(CURDIR)/junit-test_pytest_otel.xml \
		tests/test_pytest_otel.py;

## @help:test:Run the test.
.PHONY: test
it-test: virtualenv
	set -e;\
	source $(VENV)/bin/activate;\
	for test in tests/it/test_*.py; \
	do \
		$(PYTHON) -m pytest --capture=no -p pytester --runpytest=subprocess \
			--junitxml $(CURDIR)/junit-$$(basename $${test}).xml \
			$${test}; \
	done;

## @help:format:Format the code.
format: virtualenv
	source $(VENV)/bin/activate;\
	$(PYTHON) -m black src/pytest_otel tests;

## @help:test-coverage:Report coverage.
.PHONY: test-coverage
test-coverage: virtualenv
	source $(VENV)/bin/activate;\
	pytest --cov=pytest_otel --capture=no -p pytester --runpytest=subprocess tests/test_pytest_otel.py;

## @precomit:pre-commit:Run precommit hooks.
lint: virtualenv
	source $(VENV)/bin/activate;\
	pre-commit run; \
	mypy --namespace-packages src/pytest_otel; \
	mypy --namespace-packages tests;

## @help:clean:Remove Python file artifacts.
.PHONY: clean
clean:
	@echo "+ $@"
	@find . -type f -name "*.py[co]" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -name '*~' -delete
	-@rm -fr src/pytest_otel.egg-info *.egg-info build dist $(VENV) bin .tox .mypy_cache .pytest_cache otel-traces-file-output.json test_spans.json temp junit-*.xml .coverage*

## @help:build:Build the Python project package.
build: virtualenv
	source $(VENV)/bin/activate;\
	$(PYTHON) -m build

## @help:run-otel-collector:Run OpenTelemetry collector in debug mode.
.PHONY: run-otel-collector
run-otel-collector:
	mkdir -p "$(CURDIR)/temp"
	docker run --rm -p 4317:4317 -u "$(id -u):$(id -g)" \
	-v "$(CURDIR)/temp:/tmp" \
	-v "$(CURDIR)/tests/otel-collector.yaml":/otel-config.yaml \
	--name otelcol otel/opentelemetry-collector \
	--config otel-config.yaml; \

# https://upload.pypi.org/legacy/
# https://test.pypi.org/legacy/
## @help:publish REPO_URL=${REPO_URL} TWINE_USER=${TWINE_USER} TWINE_PASSWORD=${TWINE_PASSWORD}:Publish the Python project in a PyPI repository.
.PHONY: publish
publish: build
	set +xe; \
	source $(VENV)/bin/activate;\
	echo "Uploading to $${REPO_URL}";\
	$(PYTHON) -m twine upload --username "$${TWINE_USER}" --password "$${TWINE_PASSWORD}" --skip-existing --repository-url $${REPO_URL} dist/*.tar.gz;\
	$(PYTHON) -m twine upload --username "$${TWINE_USER}" --password "$${TWINE_PASSWORD}" --skip-existing --repository-url $${REPO_URL} dist/*.whl

## @help:demo-start-DEMO_NAME:Starts the demo from the demo folder, DEMO_NAME is the name of the demo type folder in the docs/demos folder (jaeger, elastic).
.PHONY: demo-start-%
demo-start-%: virtualenv
	$(MAKE) demo-stop-$*
	mkdir -p $(DEMO_DIR)/$*/build
	touch $(DEMO_DIR)/$*/build/tests.json
	docker-compose -f $(DEMO_DIR)/$*/docker-compose.yml up -d
	. $(DEMO_DIR)/$*/demo.env;\
	env | grep OTEL;\
	source $(VENV)/bin/activate;\
	$(PYTHON) -m pytest --capture=no docs/demos/test/test_demo.py || echo "Demo execution finished you can access to http://localhost:5601 to check the traces, the user is 'admin' and the password 'changeme'";

## @help:demo-stop-DEMO_NAME:Stops the demo from the demo folder, DEMO_NAME is the name of the demo type folder in the docs/demos folder (jaeger, elastic).
.PHONY: demo-stop-%
demo-stop-%:
	-docker-compose -f $(DEMO_DIR)/$*/docker-compose.yml down --remove-orphans --volumes
	-rm -fr $(DEMO_DIR)/$*/build
