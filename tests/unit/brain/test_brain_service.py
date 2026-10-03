"""Unit tests for Shared Brain service and checkpointer."""

from uuid import uuid4

import pytest

from packages.brain.checkpointer import get_memory_checkpointer
from packages.brain.service import InMemorySharedBrain, VentureConstraints, VentureProfile


@pytest.mark.asyncio
async def test_in_memory_shared_brain_lifecycle() -> None:
    """Verify storing and retrieving venture profile and constraints."""
    brain = InMemorySharedBrain()
    v_id = uuid4()
    t_id = uuid4()

    # Store profile
    profile = VentureProfile(
        id=v_id,
        tenant_id=t_id,
        name="Launchpad",
        idea="SaaS for startups",
        jurisdiction="US-WY",
        stage="validation",
    )
    brain.profiles[v_id] = profile

    # Store constraints
    constraints = VentureConstraints(
        venture_id=v_id,
        budget_cap=5000.0,
        max_cac=150.0,
        outreach_cap=1000,
    )
    brain.constraints[v_id] = constraints

    # Retrieve and verify
    fetched_profile = await brain.get_venture_profile(v_id)
    assert fetched_profile is not None
    assert fetched_profile.name == "Launchpad"

    fetched_constraints = await brain.get_active_constraints(v_id)
    assert fetched_constraints is not None
    assert fetched_constraints.budget_cap == 5000.0

    # Record decision
    dec_id = await brain.record_decision(
        venture_id=v_id,
        summary="Use Stripe for billing",
        rationale="Industry standard and hosted checkout compliance",
        evidence_refs=["doc://billing-eval"],
        decided_by="founder",
    )
    assert dec_id is not None
    assert len(brain.decisions) == 1
    assert brain.decisions[0]["summary"] == "Use Stripe for billing"


def test_memory_checkpointer_instantiation() -> None:
    """Verify LangGraph memory checkpointer returns valid instance."""
    checkpointer = get_memory_checkpointer()
    assert checkpointer is not None
