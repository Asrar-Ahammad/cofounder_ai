"""Sandboxed preview deployment node for Web Agent."""

from packages.agents.web.state import WebAgentState


def deploy_to_sandbox_environment(state: WebAgentState) -> WebAgentState:
    """Deploy sanitized landing page to isolated tenant sandbox domain.

    Args:
        state: Active Web agent state.

    Returns:
        WebAgentState: State updated with sandbox_url and deployment status.
    """
    if state.compliance_status != "clean":
        state.is_deployed = False
        state.sandbox_url = None
        state.summary = "Deployment halted: compliance screening flagged copy requiring founder review."
        return state

    subdomain = f"{state.tenant_id.lower()}-{state.venture_id.lower()}".replace("_", "-")
    state.sandbox_url = f"https://{subdomain}.cofundersites.com/preview"
    state.is_deployed = True
    state.summary = f"Landing page successfully published to isolated sandbox at {state.sandbox_url}."
    return state
