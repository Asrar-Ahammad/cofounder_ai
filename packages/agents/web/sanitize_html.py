"""HTML sanitization and defense-in-depth XSS filter for Web Agent."""

import re

from packages.agents.web.state import WebAgentState

# Regex filters stripping active scripts and inline executable handlers
_SCRIPT_TAG_RE = re.compile(r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script\s*>", re.IGNORECASE)
_EVENT_HANDLER_RE = re.compile(r"\s+on[a-zA-Z]+\s*=\s*(?:'[^']*'|\"[^\"]*\"|[^\s>]+)", re.IGNORECASE)
_JS_PROTOCOL_RE = re.compile(r"""(?:href|src)\s*=\s*['"]\s*javascript:[^'"]*['"]""", re.IGNORECASE)


def sanitize_landing_page_html(state: WebAgentState) -> WebAgentState:
    """Sanitize generated landing page HTML by stripping executable scripts and event handlers.

    Args:
        state: Active Web agent state with generated_html.

    Returns:
        WebAgentState: State updated with sanitized_html.
    """
    html = state.generated_html or ""
    # Strip script blocks
    cleaned = _SCRIPT_TAG_RE.sub("", html)
    # Strip inline on* handlers (onerror, onload, onclick, etc.)
    cleaned = _EVENT_HANDLER_RE.sub("", cleaned)
    # Strip javascript: schemes in href/src
    cleaned = _JS_PROTOCOL_RE.sub('href="#"', cleaned)

    state.sanitized_html = cleaned.strip()
    return state
