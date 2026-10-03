"""Marketing and Social Agent LangGraph subgraph builder."""

from typing import Any

from langgraph.graph import END, START, StateGraph

from packages.agents.marketing.draft_marketing_copy import draft_social_post_copy
from packages.agents.marketing.review_brand_voice import evaluate_brand_voice_fit
from packages.agents.marketing.schedule_marketing_post import schedule_or_publish_post
from packages.agents.marketing.state import MarketingState


class MarketingAgent:
    """Specialist agent generating brand-aligned social content and scheduled calendars."""

    name: str = "marketing_agent"
    allowed_tools: frozenset[str] = frozenset({"publish_social_post", "schedule_post"})
    consumes: frozenset[str] = frozenset({"campaign_requested", "venture_validated"})
    emits: frozenset[str] = frozenset({"post_drafted", "post_published"})

    def build_graph(self) -> Any:
        """Construct and compile the Marketing Agent LangGraph subgraph.

        Returns:
            CompiledStateGraph: Executable marketing content pipeline.
        """
        builder = StateGraph(MarketingState)
        builder.add_node("draft_copy", draft_social_post_copy)
        builder.add_node("review_brand_voice", evaluate_brand_voice_fit)
        builder.add_node("schedule_post", schedule_or_publish_post)

        builder.add_edge(START, "draft_copy")
        builder.add_edge("draft_copy", "review_brand_voice")
        builder.add_edge("review_brand_voice", "schedule_post")
        builder.add_edge("schedule_post", END)

        return builder.compile()
