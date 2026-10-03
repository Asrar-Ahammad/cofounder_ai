"""Unit tests for Web Agent landing page generation, sanitization, and compliance."""

import pytest

from packages.agents.web.agent import WebAgent
from packages.agents.web.deploy_sandbox import deploy_to_sandbox_environment
from packages.agents.web.generate_landing_page import generate_landing_page_html
from packages.agents.web.sanitize_html import sanitize_landing_page_html
from packages.agents.web.screen_web_content import screen_landing_page_compliance
from packages.agents.web.state import WebAgentState


def test_web_agent_generation_and_sanitization() -> None:
    """Verify HTML generation and aggressive script/handler sanitization."""
    state = WebAgentState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="AuditPulse",
        tagline="Autonomous SOC 2 Compliance",
        value_proposition="Continuous evidence collection and automated audit readiness.",
        features=[{"title": "Automated Evidence", "desc": "Syncs AWS and GitHub."}],
    )

    state = generate_landing_page_html(state)
    assert "<!DOCTYPE html>" in state.generated_html
    assert "AuditPulse" in state.generated_html
    assert "Inter" in state.generated_html

    # Inject simulated XSS payload into generated HTML
    state.generated_html += (
        '<script>alert("pwned")</script>'
        '<img src="x" onerror="alert(1)">'
        '<a href="javascript:stealCookie()">Click me</a>'
    )

    state = sanitize_landing_page_html(state)
    assert "<script>" not in state.sanitized_html
    assert "onerror=" not in state.sanitized_html
    assert "javascript:" not in state.sanitized_html


def test_web_agent_compliance_screening_and_deployment() -> None:
    """Verify compliance screener flags deceptive claims and permits clean ones."""
    clean_state = WebAgentState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="CleanApp",
        tagline="Fast Developer Documentation",
        value_proposition="Generate clean docs from source code in seconds.",
    )
    clean_state = generate_landing_page_html(clean_state)
    clean_state = sanitize_landing_page_html(clean_state)
    clean_state = screen_landing_page_compliance(clean_state)
    assert clean_state.compliance_status == "clean"

    clean_state = deploy_to_sandbox_environment(clean_state)
    assert clean_state.is_deployed is True
    assert clean_state.sandbox_url is not None
    assert "cofundersites.com/preview" in clean_state.sandbox_url

    # Flagged copy
    flagged_state = WebAgentState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="CryptoScam",
        tagline="Guaranteed ROI In 30 Days",
        value_proposition="100% risk-free profit with zero downside.",
    )
    flagged_state = generate_landing_page_html(flagged_state)
    flagged_state = sanitize_landing_page_html(flagged_state)
    flagged_state = screen_landing_page_compliance(flagged_state)
    assert flagged_state.compliance_status == "flagged"

    flagged_state = deploy_to_sandbox_environment(flagged_state)
    assert flagged_state.is_deployed is False
    assert flagged_state.sandbox_url is None
    assert "Deployment halted" in flagged_state.summary


@pytest.mark.asyncio
async def test_web_agent_graph_execution() -> None:
    """Verify Web Agent compiled LangGraph executes end-to-end."""
    agent = WebAgent()
    graph = agent.build_graph()

    state = WebAgentState(
        tenant_id="tenant_abc",
        venture_id="venture_xyz",
        venture_name="DataFlow AI",
        tagline="Real-time ETL Pipelines",
        value_proposition="Automate data streaming without complex infrastructure.",
    )

    final_state = await graph.ainvoke(state)
    assert final_state["compliance_status"] == "clean"
    assert final_state["is_deployed"] is True
    assert "tenant-abc-venture-xyz.cofundersites.com" in final_state["sandbox_url"]
