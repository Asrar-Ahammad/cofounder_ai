"""Hard-coded policy rules that cannot be relaxed or bypassed by tenants."""

# Actions that can NEVER be auto-approved, regardless of model probability
NEVER_AUTO_ACTIONS = frozenset(
    [
        "send_payment",
        "file_regulatory",
        "sign_legal",
        "execute_contract",
        "reorder_inventory",
    ]
)

# Safety-critical decision use cases that must strictly fail closed if the model is down or low confidence
FAIL_CLOSED_USE_CASES = frozenset(
    [
        "approval_risk",               # D1
        "screen_untrusted_content",    # D2
        "screen_compliance",           # D12
    ]
)


def is_never_auto(action: str) -> bool:
    """Check whether an action is prohibited from auto-approval.

    Args:
        action: The tool or action name.

    Returns:
        bool: True if human confirmation is strictly mandatory.
    """
    return action in NEVER_AUTO_ACTIONS


def is_fail_closed(use_case: str) -> bool:
    """Check whether a decision use-case must fail closed.

    Args:
        use_case: The decision identifier.

    Returns:
        bool: True if low confidence or errors require quarantine/blocking.
    """
    return use_case in FAIL_CLOSED_USE_CASES
