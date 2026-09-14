# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

"""Attribute conventions strategy for pytest_otel."""

import enum
from typing import Any

from opentelemetry import trace


class AttributeConvention(str, enum.Enum):
    """Supported attribute conventions for pytest_otel."""

    LEGACY = "legacy"
    OTEL = "otel"
    BOTH = "both"

    @classmethod
    def from_str(cls, value: str | None) -> "AttributeConvention":
        """Parse string value into AttributeConvention, defaulting to LEGACY."""
        if not value:
            return cls.LEGACY
        normalized = value.strip().lower()
        if normalized in ("legacy", "pytest"):
            return cls.LEGACY
        if normalized in ("otel", "cicd"):
            return cls.OTEL
        if normalized == "both":
            return cls.BOTH
        return cls.LEGACY


def map_suite_outcome_to_otel(outcome: str | None) -> str:
    """Map pytest outcome to OTel test.suite.run.status and cicd.pipeline.result."""
    if outcome == "passed":
        return "success"
    if outcome == "failed":
        return "failure"
    if outcome in ("interrupted", "aborted"):
        return "aborted"
    if outcome == "skipped":
        return "skipped"
    if outcome in ("internal_error", "usage_error", "no_tests_collected"):
        return "failure"
    return "failure"


def map_case_outcome_to_otel(outcome: str | None) -> str:
    """Map pytest outcome to OTel test.case.result.status."""
    if outcome == "passed":
        return "pass"
    return "fail"


def set_suite_attributes(
    span: trace.Span,
    convention: AttributeConvention,
    suite_name: str,
    outcome: str | None,
) -> None:
    """Set test suite attributes on the span according to convention."""
    if convention in (AttributeConvention.LEGACY, AttributeConvention.BOTH) and outcome is not None:
        span.set_attribute("tests.status", outcome)

    if convention in (AttributeConvention.OTEL, AttributeConvention.BOTH):
        span.set_attribute("test.suite.name", suite_name)
        if outcome is not None:
            suite_status = map_suite_outcome_to_otel(outcome)
            span.set_attribute("test.suite.run.status", suite_status)
            span.set_attribute("cicd.pipeline.result", suite_status)
            if suite_status in ("failure", "aborted", "error"):
                span.set_attribute("error.type", outcome)


def set_test_start_attributes(
    span: trace.Span,
    convention: AttributeConvention,
    test_name: str,
    nodeid: str | None = None,
) -> None:
    """Set test case start attributes on the span according to convention."""
    if convention in (AttributeConvention.LEGACY, AttributeConvention.BOTH):
        span.set_attribute("tests.name", test_name)

    if convention in (AttributeConvention.OTEL, AttributeConvention.BOTH):
        qualified_name = nodeid if nodeid else test_name
        span.set_attribute("test.case.name", qualified_name)
        span.set_attribute("cicd.pipeline.task.name", test_name)


def set_test_outcome_attributes(
    span: trace.Span,
    convention: AttributeConvention,
    outcome: str | None,
) -> None:
    """Set test case outcome attributes on the span according to convention."""
    if convention in (AttributeConvention.LEGACY, AttributeConvention.BOTH):
        span.set_attribute("tests.status", f"{outcome}")

    if convention in (AttributeConvention.OTEL, AttributeConvention.BOTH):
        case_status = map_case_outcome_to_otel(outcome)
        task_status = map_suite_outcome_to_otel(outcome)
        span.set_attribute("test.case.result.status", case_status)
        span.set_attribute("cicd.pipeline.task.run.result", task_status)
        if case_status == "fail":
            span.set_attribute("error.type", outcome if outcome else "_OTHER")


def set_test_exception_attributes(
    span: trace.Span,
    convention: AttributeConvention,
    message: str | None = None,
    error_stack: str | None = None,
    exception_type: str | None = None,
) -> None:
    """Set test exception / error attributes on the span according to convention."""
    if convention in (AttributeConvention.LEGACY, AttributeConvention.BOTH):
        if message is not None:
            span.set_attribute("tests.message", message)
        if error_stack is not None:
            span.set_attribute("tests.error", error_stack)

    if convention in (AttributeConvention.OTEL, AttributeConvention.BOTH):
        if message is not None:
            span.set_attribute("exception.message", message)
        if error_stack is not None:
            span.set_attribute("exception.stacktrace", error_stack)
        if exception_type is not None:
            span.set_attribute("exception.type", exception_type)
            span.set_attribute("error.type", exception_type)


def set_test_teardown_attributes(
    span: trace.Span,
    convention: AttributeConvention,
    system_err: Any,
    system_out: Any,
    duration: float,
) -> None:
    """Set test teardown attributes (stdout, stderr, duration) on the span according to convention."""
    if convention in (AttributeConvention.LEGACY, AttributeConvention.BOTH):
        span.set_attribute("tests.systemerr", system_err)
        span.set_attribute("tests.systemout", system_out)
        span.set_attribute("tests.duration", duration)

    if convention in (AttributeConvention.OTEL, AttributeConvention.BOTH):
        if system_err:
            span.set_attribute("test.case.systemerr", str(system_err))
        if system_out:
            span.set_attribute("test.case.systemout", str(system_out))
        span.set_attribute("test.case.duration", duration)
