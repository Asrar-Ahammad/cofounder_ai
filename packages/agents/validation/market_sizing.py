"""Market sizing calculation engine for TAM, SAM, and SOM."""

from packages.agents.validation.state import MarketSizeResult, ValidationState


def calculate_market_sizing(state: ValidationState) -> ValidationState:
    """Calculate TAM, SAM, and SOM using transparent top-down and bottom-up formulas.

    Args:
        state: Active Validation state with market_size_inputs.

    Returns:
        ValidationState: State updated with market size calculations.
    """
    inputs = state.market_size_inputs
    total_customers = float(inputs.get("total_addressable_customers", 100000))
    target_geo_pct = float(inputs.get("target_geography_percentage", 0.30))
    obtainable_pct = float(inputs.get("year_3_obtainable_percentage", 0.05))
    acv = float(inputs.get("annual_contract_value", 1200))

    tam = total_customers * acv
    sam = tam * target_geo_pct
    som = sam * obtainable_pct

    formula = (
        f"TAM = {total_customers:,.0f} units * ${acv:,.2f} ACV = ${tam:,.2f}. "
        f"SAM = TAM * {target_geo_pct * 100:.1f}% geo focus = ${sam:,.2f}. "
        f"SOM = SAM * {obtainable_pct * 100:.1f}% obtainable = ${som:,.2f}."
    )

    state.market_size = MarketSizeResult(
        tam=tam,
        sam=sam,
        som=som,
        formula_explanation=formula,
    )
    return state
