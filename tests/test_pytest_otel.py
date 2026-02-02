# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

import pytest
import json

pytest_plugins = ["pytester"]

common_code = """
import time
import logging
import pytest

"""


def assertTestSuit(span, outcome, status):
    assert span["kind"] == "SpanKind.SERVER"
    assert span["status"]["status_code"] == status
    if outcome is not None:
        assert span["attributes"]["tests.status"] == outcome
    assert span["parent_id"] is None
    return True


def assertSpan(span, name, outcome, status):
    assert span["kind"] == "SpanKind.INTERNAL"
    assert span["status"]["status_code"] == status
    assert span["attributes"]["tests.name"] == name
    if outcome is not None:
        assert span["attributes"]["tests.status"] == outcome
    assert len(span["parent_id"]) > 0
    return True


def assertTest(pytester, name, ts_outcome, ts_status, outcome, status):
    pytester.runpytest("--otel-span-file-output=./test_spans.json", "--otel-debug=True", "-rsx")
    span_list = None
    with open("test_spans.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    foundTest = False
    foundTestSuit = False
    for span in span_list:
        if span["name"] == "Running {}".format(name):
            foundTest = assertSpan(span, name, outcome, status)
        if span["name"] == "Test Suite":
            foundTestSuit = assertTestSuit(span, ts_outcome, ts_status)
    assert foundTest or name is None
    assert foundTestSuit


def test_basic_plugin(pytester):
    """test a simple test"""
    pytester.makepyfile(
        common_code
        + """
def test_basic():
    time.sleep(5)
    pass
"""
    )
    assertTest(pytester, "test_basic", "passed", "OK", "passed", "OK")


def test_success_plugin(pytester):
    """test a success test"""
    pytester.makepyfile(
        common_code
        + """
def test_success():
    assert True
"""
    )
    assertTest(pytester, "test_success", "passed", "OK", "passed", "OK")


def test_failure_plugin(pytester):
    """test a failed test"""
    pytester.makepyfile(
        common_code
        + """
def test_failure():
    assert 1 < 0
"""
    )
    assertTest(pytester, "test_failure", "failed", "ERROR", "failed", "ERROR")


def test_failure_code_plugin(pytester):
    """test a test with a code exception"""
    pytester.makepyfile(
        common_code
        + """
def test_failure_code():
    d = 1/0
    pass
"""
    )
    assertTest(pytester, "test_failure_code", "failed", "ERROR", "failed", "ERROR")


def test_skip_plugin(pytester):
    """test a skipped test"""
    pytester.makepyfile(
        common_code
        + """
@pytest.mark.skip
def test_skip():
    assert True
"""
    )
    assertTest(pytester, None, "passed", "OK", None, None)


def test_xfail_plugin(pytester):
    """test a marked as xfail test"""
    pytester.makepyfile(
        common_code
        + """
@pytest.mark.xfail(reason="foo bug")
def test_xfail():
    assert False
"""
    )
    assertTest(pytester, None, "passed", "OK", None, None)


def test_xfail_no_run_plugin(pytester):
    """test a marked as xfail test with run==false"""
    pytester.makepyfile(
        common_code
        + """
@pytest.mark.xfail(run=False)
def test_xfail_no_run():
    assert False
"""
    )
    assertTest(pytester, None, "passed", "OK", None, None)


def test_http_exporter_protocol(pytester):
    """test that http exporter protocol option works"""
    # Note: This test verifies that the --otel-exporter-protocol=http/protobuf flag is accepted
    # and the HTTP exporter can be initialized without errors. Since no endpoint is configured,
    # the in-memory exporter is used instead of making actual network calls.
    pytester.makepyfile(
        common_code
        + """
def test_http_protocol():
    assert True
"""
    )
    pytester.runpytest(
        "--otel-span-file-output=./test_spans_http.json",
        "--otel-debug=True",
        "--otel-exporter-protocol=http/protobuf",
        "-rsx",
    )
    span_list = None
    with open("test_spans_http.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    foundTest = False
    foundTestSuit = False
    for span in span_list:
        if span["name"] == "Running test_http_protocol":
            foundTest = assertSpan(span, "test_http_protocol", "passed", "OK")
        if span["name"] == "Test Suite":
            foundTestSuit = assertTestSuit(span, "passed", "OK")
    assert foundTest
    assert foundTestSuit


def test_dotenv_integration(pytester):
    """test that dotenv file loading works for environment variables"""
    # Create a dotenv file with test configuration
    # Note: OTEL_SERVICE_NAME and OTEL_EXPORTER_OTLP_PROTOCOL will be overridden by CLI defaults
    # The dotenv is useful for other OTEL env vars like OTEL_RESOURCE_ATTRIBUTES
    pytester.makefile(
        ".env",
        otel="""OTEL_RESOURCE_ATTRIBUTES=service.version=1.0.0,deployment.environment=test
""",
    )
    pytester.makepyfile(
        common_code
        + """
import os

def test_dotenv_loaded():
    # Verify that environment variables from dotenv are loaded
    # OTEL_RESOURCE_ATTRIBUTES should be set from dotenv
    resource_attrs = os.environ.get("OTEL_RESOURCE_ATTRIBUTES")
    assert resource_attrs is not None, "OTEL_RESOURCE_ATTRIBUTES should be set from dotenv"
    assert "service.version=1.0.0" in resource_attrs
    assert "deployment.environment=test" in resource_attrs
    assert True
"""
    )
    pytester.runpytest(
        "--otel-dotenv-path=otel.env",
        "--otel-span-file-output=./test_spans_dotenv.json",
        "--otel-debug=True",
        "-rsx",
    )
    span_list = None
    with open("test_spans_dotenv.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    foundTest = False
    foundTestSuit = False
    for span in span_list:
        if span["name"] == "Running test_dotenv_loaded":
            foundTest = assertSpan(span, "test_dotenv_loaded", "passed", "OK")
        if span["name"] == "Test Suite":
            foundTestSuit = assertTestSuit(span, "passed", "OK")
    assert foundTest
    assert foundTestSuit


def test_dotenv_cli_precedence(pytester):
    """test that CLI flags take precedence over dotenv values"""
    # Create a dotenv file with service name and protocol
    pytester.makefile(
        ".env",
        otel="""OTEL_SERVICE_NAME=dotenv-service
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_RESOURCE_ATTRIBUTES=service.version=1.0.0,deployment.environment=test
""",
    )
    pytester.makepyfile(
        common_code
        + """
import os

def test_cli_override():
    # Verify that CLI flags override dotenv values
    # Service name should be 'cli-service' from CLI, not 'dotenv-service' from dotenv
    service_name = os.environ.get("OTEL_SERVICE_NAME")
    assert service_name == "cli-service", f"Expected 'cli-service', got '{service_name}'"

    # Protocol should be 'grpc' from CLI, not 'http/protobuf' from dotenv
    protocol = os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL")
    assert protocol == "grpc", f"Expected 'grpc', got '{protocol}'"

    # Resource attributes should still come from dotenv (not overridden by CLI)
    resource_attrs = os.environ.get("OTEL_RESOURCE_ATTRIBUTES")
    assert resource_attrs is not None
    assert "service.version=1.0.0" in resource_attrs
    assert True
"""
    )
    pytester.runpytest(
        "--otel-dotenv-path=otel.env",
        "--otel-service-name=cli-service",
        "--otel-exporter-protocol=grpc",
        "--otel-span-file-output=./test_spans_precedence.json",
        "--otel-debug=True",
        "-rsx",
    )
    span_list = None
    with open("test_spans_precedence.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    foundTest = False
    foundTestSuit = False
    for span in span_list:
        if span["name"] == "Running test_cli_override":
            foundTest = assertSpan(span, "test_cli_override", "passed", "OK")
        if span["name"] == "Test Suite":
            foundTestSuit = assertTestSuit(span, "passed", "OK")
    assert foundTest
    assert foundTestSuit


def test_dotenv_missing_file(pytester, capsys):
    """test that missing dotenv file is handled gracefully"""
    # Don't create a dotenv file, but specify a path that doesn't exist
    pytester.makepyfile(
        common_code
        + """
def test_missing_file():
    # Test should run successfully even if dotenv file is missing
    assert True
"""
    )
    result = pytester.runpytest(
        "--otel-dotenv-path=nonexistent.env",
        "--otel-span-file-output=./test_spans_missing.json",
        "--otel-debug=True",
        "-rsx",
    )
    # Test should pass even without the dotenv file
    result.assert_outcomes(passed=1)
    span_list = None
    with open("test_spans_missing.json", encoding="utf-8") as input:
        span_list = json.loads(input.read())
    foundTest = False
    foundTestSuit = False
    for span in span_list:
        if span["name"] == "Running test_missing_file":
            foundTest = assertSpan(span, "test_missing_file", "passed", "OK")
        if span["name"] == "Test Suite":
            foundTestSuit = assertTestSuit(span, "passed", "OK")
    assert foundTest
    assert foundTestSuit


def test_dotenv_complex_variables(pytester):
    """test that multiple complex OTEL environment variables are loaded correctly"""
    # Create a dotenv file with multiple OTEL SDK configuration variables
    pytester.makefile(
        ".env",
        otel="""OTEL_RESOURCE_ATTRIBUTES=service.name=test-service,service.version=1.2.3,deployment.environment=staging,service.instance.id=instance-123
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
OTEL_EXPORTER_OTLP_HEADERS=api-key=secret123,x-custom-header=value456
OTEL_METRIC_EXPORT_INTERVAL=10000
OTEL_BSP_SCHEDULE_DELAY=2000
OTEL_BSP_MAX_QUEUE_SIZE=4096
OTEL_TRACES_SAMPLER=parentbased_always_on
OTEL_PROPAGATORS=tracecontext,baggage
""",
    )
    pytester.makepyfile(
        common_code
        + """
import os

def test_complex_vars():
    # Verify that all OTEL environment variables from dotenv are loaded
    resource_attrs = os.environ.get("OTEL_RESOURCE_ATTRIBUTES")
    assert resource_attrs is not None
    assert "service.name=test-service" in resource_attrs
    assert "service.version=1.2.3" in resource_attrs
    assert "deployment.environment=staging" in resource_attrs
    assert "service.instance.id=instance-123" in resource_attrs

    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT")
    assert endpoint == "http://localhost:4318"

    headers = os.environ.get("OTEL_EXPORTER_OTLP_HEADERS")
    assert headers is not None
    assert "api-key=secret123" in headers
    assert "x-custom-header=value456" in headers

    metric_interval = os.environ.get("OTEL_METRIC_EXPORT_INTERVAL")
    assert metric_interval == "10000"

    bsp_delay = os.environ.get("OTEL_BSP_SCHEDULE_DELAY")
    assert bsp_delay == "2000"

    queue_size = os.environ.get("OTEL_BSP_MAX_QUEUE_SIZE")
    assert queue_size == "4096"

    sampler = os.environ.get("OTEL_TRACES_SAMPLER")
    assert sampler == "parentbased_always_on"

    propagators = os.environ.get("OTEL_PROPAGATORS")
    assert propagators == "tracecontext,baggage"

    assert True
"""
    )
    result = pytester.runpytest(
        "--otel-dotenv-path=otel.env",
        "--otel-span-file-output=./test_spans_complex.json",
        "--otel-debug=True",
        "-rsx",
    )
    # Verify test passed
    result.assert_outcomes(passed=1)
    # Note: We don't verify span file contents for this test since the main goal
    # is to verify that complex OTEL environment variables are loaded correctly,
    # which is tested by the assertions in test_complex_vars itself
