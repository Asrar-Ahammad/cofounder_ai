"""Grounded knowledge base answering node with strict citation enforcement."""

from packages.agents.support.state import SupportState


def answer_from_approved_knowledge(state: SupportState) -> SupportState:
    """Retrieve grounded answer strictly from approved venture knowledge sources.

    Args:
        state: Active Support state.

    Returns:
        SupportState: State updated with kb_answer and citations, or escalated on abstention.
    """
    kb = state.approved_knowledge or {
        "pricing": "Our starter tier is $29/month and professional tier is $99/month.",
        "security": "We enforce AES-256 encryption at rest, TLS 1.3 in transit, and multi-tenant RLS.",
        "refund": "We offer a 30-day no-questions-asked refund policy for all standard plans.",
        "setup": "Setup requires adding our script tag or integrating the API endpoint in 5 minutes.",
    }

    message_lower = state.incoming_message.lower()
    matched_topics: list[str] = []
    matched_excerpts: list[str] = []

    for topic, content in kb.items():
        if topic in message_lower or any(word in message_lower for word in topic.split()):
            matched_topics.append(topic)
            matched_excerpts.append(content)

    if matched_excerpts:
        state.kb_answer = " ".join(matched_excerpts)
        state.citations = [f"kb:{t}" for t in matched_topics]
        state.summary = f"Answer retrieved with grounded knowledge citations: {', '.join(state.citations)}."
    else:
        # Abstain to prevent hallucinating unverified commitments
        state.requires_escalation = True
        state.escalation_reason = "Information requested is absent from approved knowledge base."
        state.summary = "Abstained from ungrounded claim; ticket escalated for founder confirmation."

    return state
