"""Unit tests for Marketing and Social Agent LangGraph subgraph."""

import pytest

from packages.agents.marketing.agent import MarketingAgent
from packages.agents.marketing.draft_marketing_copy import draft_social_post_copy
from packages.agents.marketing.review_brand_voice import evaluate_brand_voice_fit
from packages.agents.marketing.schedule_marketing_post import schedule_or_publish_post
from packages.agents.marketing.state import MarketingState


def test_marketing_agent_draft_and_approval_flow() -> None:
    """Verify clean marketing draft passes review and stages for approval."""
    state = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="AuditPulse",
        campaign_goal="Announce continuous SOC 2 evidence automation",
        platform="linkedin",
        needs_approval=True,
    )

    state = draft_social_post_copy(state)
    assert "AuditPulse" in state.draft_copy
    assert len(state.tags) > 0

    state = evaluate_brand_voice_fit(state)
    assert state.brand_fit_decision == "pass"

    state = schedule_or_publish_post(state)
    assert state.published_id is None
    assert "awaiting founder approval" in state.summary

    # Founder grants approval
    state.needs_approval = False
    state = schedule_or_publish_post(state)
    assert state.published_id is not None
    assert "pub-linkedin-v1" in state.published_id


def test_marketing_agent_rejects_off_brand_hype() -> None:
    """Verify review node flags informal and unverified hype phrases."""
    state = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="ScamCoin",
        campaign_goal="Promote rapid token appreciation",
        draft_copy="Get rich quick with 100x gains guaranteed profit!",
        platform="x",
    )

    state = evaluate_brand_voice_fit(state)
    assert state.brand_fit_decision == "revise"
    assert "informal or unverified hype" in state.summary

    state = schedule_or_publish_post(state)
    assert state.published_id is None
    assert "requires brand voice revision" in state.summary


@pytest.mark.asyncio
async def test_marketing_agent_graph_execution() -> None:
    """Verify Marketing Agent compiled LangGraph executes end-to-end."""
    agent = MarketingAgent()
    graph = agent.build_graph()

    state = MarketingState(
        tenant_id="t1",
        venture_id="v1",
        venture_name="DataFlow",
        campaign_goal="Share customer milestone of 10M records synced",
        platform="x",
        needs_approval=False,
    )

    final = await graph.ainvoke(state)
    assert final["brand_fit_decision"] == "pass"
    assert final["published_id"] is not None
    assert "pub-x-" in final["published_id"]
