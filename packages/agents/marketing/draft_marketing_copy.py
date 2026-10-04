"""Social and marketing post generation node for Marketing Agent."""

from packages.agents.marketing.state import MarketingState


def draft_social_post_copy(state: MarketingState) -> MarketingState:
    """Generate platform-tailored social copy based on campaign goal and platform.

    Args:
        state: Active Marketing state.

    Returns:
        MarketingState: State updated with draft copy and platform tags.
    """
    v_name = state.venture_name
    goal = state.campaign_goal
    platform = state.platform.lower()

    if platform == "x":
        copy = (
            f"Building {v_name}: {goal}.\n\n"
            "We're rethinking how startups scale with autonomous intelligence. "
            "Follow our journey."
        )
        tags = ["#buildinpublic", "#startups", "#AI"]
    else:  # linkedin, meta default
        copy = (
            f"At {v_name}, our mission is clear: {goal}.\n\n"
            "Early-stage ventures fail not from lack of ambition, but from operational drag. "
            "By pairing human judgment with autonomous execution, we're giving founders their time back.\n\n"
            "What has been your biggest bottleneck this quarter?"
        )
        tags = ["#Founders", "#StartupLife", "#Innovation", "#ArtificialIntelligence"]

    state.draft_copy = copy
    state.tags = tags
    state.summary = f"Drafted {platform.upper()} marketing copy for campaign goal: '{goal}'."
    return state
