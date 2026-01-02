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
    """test that dotenv file loading works"""
    # Create a dotenv file with test configuration
    pytester.makefile(
        ".env",
        otel="""OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=TestServiceFromDotenv
""",
    )
    pytester.makepyfile(
        common_code
        + """
import os

def test_dotenv_loaded():
    # Verify that environment variables from dotenv are loaded
    assert os.environ.get("OTEL_EXPORTER_OTLP_PROTOCOL") == "http/protobuf"
    assert os.environ.get("OTEL_SERVICE_NAME") == "TestServiceFromDotenv"
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
