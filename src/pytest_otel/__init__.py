# Copyright The OpenTelemetry Authors
# SPDX-License-Identifier: Apache-2.0

import logging
import os
import sys
import traceback
from collections.abc import Generator
from typing import Any

import _pytest._code
import _pytest.skipping
import pytest
from opentelemetry import trace
from opentelemetry.context import Context
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor, SpanExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.trace.status import Status, StatusCode

from pytest_otel.conventions import (
    AttributeConvention,
    set_suite_attributes,
    set_test_exception_attributes,
    set_test_outcome_attributes,
    set_test_start_attributes,
    set_test_teardown_attributes,
)

__version__ = "2.4.0"

LOGGER = logging.getLogger("pytest_otel")
service_name: str | None = None
traceparent: str | None = None
session_name: str | None = None
tracer: trace.Tracer | None = None
insecure: bool | str | None = None
in_memory_span_exporter: bool = False
otel_span_file_output: str | None = None
otel_exporter: SpanExporter | None = None
otel_exporter_protocol: str | None = None
spans: dict[str, trace.Span] = {}
outcome: str | None = None
otel_debug: bool = False
attribute_convention: AttributeConvention = AttributeConvention.LEGACY


def pytest_addoption(parser: pytest.Parser) -> None:
    """Init command line arguments"""
    group = parser.getgroup("pytest-otel", "report OpenTelemetry traces for tests executed.")

    group.addoption(
        "--otel-endpoint",
        dest="endpoint",
        help="URL for the APM server.(OTEL_EXPORTER_OTLP_ENDPOINT)",
    )
    group.addoption(
        "--otel-headers",
        dest="headers",
        help="Additional headers to send (i.e.: key1=value1,key2=value2).(OTEL_EXPORTER_OTLP_HEADERS)",  # noqa: E501
    )
    group.addoption(
        "--otel-service-name",
        dest="service_name",
        default="Pytest_Otel_reporter",
        help="Name of the service.(OTEL_SERVICE_NAME)",
    )
    group.addoption(
        "--otel-session-name",
        dest="session_name",
        default="Test Suite",
        help="Name for the Main span reported.",
    )
    group.addoption(
        "--otel-traceparent",
        dest="traceparent",
        help="Trace parent.(TRACEPARENT) see https://www.w3.org/TR/trace-context-1/#trace-context-http-headers-format",  # noqa: E501
    )
    group.addoption(
        "--otel-insecure",
        dest="insecure",
        default=False,
        help="Disables TLS.(OTEL_EXPORTER_OTLP_INSECURE)",
    )
    group.addoption(
        "--otel-span-file-output",
        dest="otel_span_file_output",
        default="./otel-traces-file-output.json",
        help="If the Otel endpoint is not set, the spans will be saved to a file (./otel-traces-file-output.txt)",
    )
    group.addoption(
        "--otel-debug",
        dest="otel_debug",
        default=False,
        help="",
    )
    group.addoption(
        "--otel-exporter-protocol",
        dest="otel_exporter_protocol",
        default="grpc",
        help="OTLP exporter protocol: 'grpc' or 'http/protobuf'. Default is 'grpc'.(OTEL_EXPORTER_OTLP_PROTOCOL)",
    )
    group.addoption(
        "--otel-dotenv-path",
        dest="otel_dotenv_path",
        default=None,
        help="Path to a dotenv file to load environment variables from.",
    )
    group.addoption(
        "--otel-attribute-convention",
        dest="otel_attribute_convention",
        default=None,
        help="Attribute convention: 'legacy', 'otel', or 'both'. Default is 'legacy'.(OTEL_ATTRIBUTE_CONVENTION)",
    )


def init_otel() -> None:
    """Init the OpenTelemetry settings"""
    global tracer, otel_exporter
    LOGGER.debug(f"Init Otel : {service_name}")
    assert service_name is not None
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: service_name}),
        )
    )

    if in_memory_span_exporter:
        otel_exporter = InMemorySpanExporter()
        trace.get_tracer_provider().add_span_processor(  # type: ignore[attr-defined]
            SimpleSpanProcessor(otel_exporter)
        )
    else:
        # Select the exporter based on the protocol
        if otel_exporter_protocol == "http/protobuf":
            from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
                OTLPSpanExporter as OTLPSpanExporter,
            )
        elif otel_exporter_protocol == "grpc":
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[assignment]
                OTLPSpanExporter as OTLPSpanExporter,
            )
        else:
            LOGGER.warning(
                f"Unknown protocol '{otel_exporter_protocol}', defaulting to 'grpc'. "
                "Valid values are 'grpc' or 'http/protobuf'."
            )
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (  # type: ignore[assignment]
                OTLPSpanExporter as OTLPSpanExporter,
            )

        otel_exporter = OTLPSpanExporter()
        trace.get_tracer_provider().add_span_processor(  # type: ignore[attr-defined]
            BatchSpanProcessor(otel_exporter)
        )

    assert session_name is not None
    tracer = trace.get_tracer(session_name)


def start_span(
    span_name: str,
    context: Context | None = None,
    kind: trace.SpanKind = trace.SpanKind.INTERNAL,
) -> trace.Span:
    """Starts a span with the name, context, and kind passed as parameters"""
    assert tracer is not None
    spans[span_name] = tracer.start_span(
        span_name, context=context, record_exception=True, set_status_on_exception=True, kind=kind
    )
    LOGGER.debug(f"The {span_name} transaction start_span.")
    return spans[span_name]


def end_span(span_name: str, outcome: str) -> trace.Span:
    """Ends a span identified by its name"""
    status = convertOutcome(outcome)
    spans[span_name].set_status(status)
    set_suite_attributes(spans[span_name], attribute_convention, span_name, outcome)
    spans[span_name].end()
    LOGGER.debug(f"The {span_name} transaction ends. -> {status}")
    return spans[span_name]


def convertOutcome(outcome: str | None) -> Status:
    """Convert from pytest outcome to OpenTelemetry status code"""
    if outcome == "passed":
        return Status(status_code=StatusCode.OK)
    elif (
        outcome == "failed"
        or outcome == "interrupted"
        or outcome == "internal_error"
        or outcome == "usage_error"
        or outcome == "no_tests_collected"
    ):
        return Status(status_code=StatusCode.ERROR)
    else:
        return Status(status_code=StatusCode.UNSET)


def exitCodeToOutcome(exit_code: int) -> str:
    """convert pytest ExitCode to outcome"""
    if exit_code == 0:  # noqa: SIM116
        return "passed"
    elif exit_code == 1:
        return "failed"
    elif exit_code == 2:
        return "interrupted"
    elif exit_code == 3:
        return "internal_error"
    elif exit_code == 4:
        return "usage_error"
    elif exit_code == 4:
        return "no_tests_collected"
    else:
        return "failed"


def traceparent_context(traceparent: str | None) -> Context:
    """Extracts the trace context from the TRACEPARENT passed"""
    carrier = {}
    carrier["traceparent"] = traceparent
    return TraceContextTextMapPropagator().extract(carrier=carrier)


def pytest_sessionstart(session: pytest.Session) -> None:
    """Uses the commandline parameter to define the environment variables used by OpenTelemetry"""
    global service_name, traceparent, session_name, insecure, in_memory_span_exporter
    global otel_span_file_output, otel_debug, otel_exporter_protocol, attribute_convention
    config = session.config

    # Load dotenv file if specified
    # When --otel-dotenv-path is used, dotenv values take precedence over inherited environment variables
    # This allows the dotenv file to be the primary source of configuration
    dotenv_path = config.getoption("otel_dotenv_path")
    if dotenv_path is not None:
        try:
            from dotenv import load_dotenv

            # Use override=True so dotenv values take precedence
            # This is intentional: when using --otel-dotenv-path, the dotenv file should be the primary config source
            result = load_dotenv(dotenv_path, override=True)
            if result:
                LOGGER.debug(f"Loaded environment variables from {dotenv_path}")
            else:
                LOGGER.warning(f"Could not load dotenv file from {dotenv_path}")
        except ImportError:
            LOGGER.warning("python-dotenv is not installed. Install it with: pip install pytest-otel[dotenv]")
        except Exception as e:
            LOGGER.warning(f"Failed to load dotenv file from {dotenv_path}: {e}")

    if config.getoption("otel_debug"):
        LOGGER.setLevel(logging.DEBUG)
        otel_debug = True
    service_name = config.getoption("service_name")
    session_name = config.getoption("session_name")
    traceparent = config.getoption("traceparent")
    endpoint = config.getoption("endpoint")
    headers = config.getoption("headers")
    insecure = config.getoption("insecure")
    otel_exporter_protocol = config.getoption("otel_exporter_protocol")

    convention_opt = config.getoption("otel_attribute_convention")
    if convention_opt is None:
        convention_opt = os.getenv("OTEL_ATTRIBUTE_CONVENTION", os.getenv("OTEL_SEMCONV_CONVENTION", None))
    attribute_convention = AttributeConvention.from_str(convention_opt)

    # Precedence order:
    # 1. CLI options (including defaults) - always take highest priority
    # 2. Environment variables from dotenv or shell - for vars not managed by CLI
    # 3. Defaults are included in CLI options above

    # endpoint has no default, so only set if explicitly provided
    if endpoint is not None:
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = endpoint

    # headers has no default, so only set if explicitly provided
    if headers is not None:
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = headers

    # service_name has a default, but check if not None for consistency
    # CLI value (including default) takes precedence over environment variables
    if service_name is not None:
        os.environ["OTEL_SERVICE_NAME"] = service_name

    # insecure has a default (False), only set if explicitly enabled
    if insecure and insecure != "False":  # Handle both bool and string
        os.environ["OTEL_EXPORTER_OTLP_INSECURE"] = "True"

    # traceparent has no default, read from env if not provided via CLI
    if traceparent is None:
        traceparent = os.getenv("TRACEPARENT", None)

    # protocol: CLI value (including default) always takes precedence
    # Set to environment variable so OpenTelemetry SDK can access it
    # This MUST be unconditional to ensure CLI flags override dotenv values
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = otel_exporter_protocol

    if len(os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "")) == 0:
        in_memory_span_exporter = True
        otel_span_file_output = config.getoption("otel_span_file_output")
    init_otel()
    start_span(session_name, traceparent_context(traceparent), trace.SpanKind.SERVER)


def pytest_runtest_setup(item: pytest.Item) -> None:  # noqa: U100
    """Clean the global outcome on every test"""
    global outcome
    outcome = None


def pytest_report_teststatus(report: pytest.TestReport) -> None:
    """Set the final outcome to the reported outcome"""
    global outcome
    outcome = report.outcome


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:  # noqa: U100
    """Ends the parent Opentelemetry span with the session outcome"""
    LOGGER.debug("Session transaction Ends")
    assert session_name is not None
    end_span(session_name, exitCodeToOutcome(exitstatus))
    LOGGER.debug(f"in_memory_span_exporter {in_memory_span_exporter}")
    if in_memory_span_exporter:
        print()
        print("Using on memory OpenTelemetry exporter")
        assert isinstance(otel_exporter, InMemorySpanExporter)
        span_list = otel_exporter.get_finished_spans()
        print(f"Number of spans: {len(span_list)}")
        if otel_debug:
            json = "[\n"
            for i in range(len(span_list)):
                if i > 0:
                    json += ","
                json += span_list[i].to_json()
            json += "\n]\n"
            assert otel_span_file_output is not None
            with open(otel_span_file_output, "w", encoding="utf-8") as output:
                output.write(json)
            print(json)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None, None, None]:
    global outcome
    assert tracer is not None
    assert session_name is not None
    with tracer.start_as_current_span(
        f"Running {item.name}",
        context=trace.set_span_in_context(spans[session_name]),
        record_exception=True,
        set_status_on_exception=True,
    ) as span:
        LOGGER.debug(f"Test {item.name} starts - {span.get_span_context()}")
        set_test_start_attributes(span, attribute_convention, item.name, getattr(item, "nodeid", None))
        info: Any = yield
        LOGGER.debug(f"Test {item.name} ends - {span.get_span_context()}")

        if hasattr(info, "_excinfo") and info._excinfo:
            (info_class, info_msg, info_trace) = info._excinfo
            if info_class.__name__ == "Failed":
                outcome = "failed"
                set_test_exception_attributes(
                    span,
                    attribute_convention,
                    message=f"{info_msg}",
                    exception_type=getattr(info_class, "__name__", None),
                )
        if hasattr(sys, "last_value") and hasattr(sys, "last_traceback") and hasattr(sys, "last_type"):
            longrepr: Any = ""
            last_value: Any = sys.last_value
            last_traceback = sys.last_traceback
            last_type = sys.last_type

            if not isinstance(last_value, _pytest._code.ExceptionInfo):
                outcome = "failed"
                longrepr = last_value
            elif isinstance(last_value, _pytest._code.skip.Exception):  # type: ignore[attr-defined]
                outcome = "skipped"
                r = last_value._getreprcrash()
                longrepr = (str(r.path), r.lineno, r.message)
            else:
                outcome = "failed"
                style = item.config.getoption("tbstyle", "auto")
                longrepr = item._repr_failure_py(last_value, style=style)  # type: ignore[attr-defined]

            stack_trace = repr(traceback.format_exception(last_type, last_value, last_traceback))
            err_msg: str | None = None
            if hasattr(last_value, "args") and len(getattr(last_value, "args", [])) > 0:
                err_msg = f"{last_value.args[0]}"
            elif longrepr:
                err_msg = f"{longrepr}"
            elif last_value:
                err_msg = f"{last_value}"
            elif last_type:
                err_msg = f"{last_type}"

            skipping = getattr(_pytest, "skipping", None)
            if skipping:
                key = getattr(skipping, "xfailed_key", None)
                xfailed = item._store.get(key, None)  # type: ignore[attr-defined,arg-type]
                reason = getattr(xfailed, "reason", None)
                if reason:
                    err_msg = f"{reason}"

            exc_type_name = getattr(last_type, "__name__", str(last_type)) if last_type else None
            set_test_exception_attributes(
                span,
                attribute_convention,
                message=err_msg,
                error_stack=stack_trace,
                exception_type=exc_type_name,
            )

        status = convertOutcome(outcome)
        span.set_status(status)
        set_test_outcome_attributes(span, attribute_convention, outcome)


@pytest.hookimpl()
def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    test_name = report.nodeid.split("::")[0]

    if report.failed and report.when == "teardown":
        try:
            span = spans[test_name]
            set_test_teardown_attributes(
                span,
                attribute_convention,
                report.capstderr,
                report.capstdout,
                getattr(report, "duration", 0.0),
            )

        except KeyError:
            LOGGER.warning(f"Ignoring unknown test during teardown: {test_name}")
