"""
Tracing setup for the service desk agents.

Call configure_tracing() once at the start of any agent script, before
making model or Graph API calls, so every call is captured as a trace
in Application Insights.
"""
import os

from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

TRACER_NAME = "euc-agentops-hack.servicedesk"


def configure_tracing() -> trace.Tracer:
    connection_string = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if not connection_string:
        raise RuntimeError(
            "Set APPLICATIONINSIGHTS_CONNECTION_STRING in your .env "
            "(Foundry portal -> Tracing -> connection string)."
        )

    configure_azure_monitor(connection_string=connection_string)
    return trace.get_tracer(TRACER_NAME)


# Example usage inside an agent script:
#
#   from tracing_setup import configure_tracing
#   tracer = configure_tracing()
#
#   with tracer.start_as_current_span("remediation.sync_device") as span:
#       span.set_attribute("device_id", device_id)
#       span.set_attribute("ticket_id", ticket_id)
#       result = sync_device(device_id)
#       span.set_attribute("result", result)
