# tests/test_model.py
from giga_atom.simulations import compute_excess_and_lambda, baseline_counts

# Type hints for imported functions (for type checkers)
from typing import Callable, List, Any
compute_excess_and_lambda: Callable[[Any, float], list]
baseline_counts: Callable[[], list]

def test_baseline_no_excess():
    counts = baseline_counts()
    states = compute_excess_and_lambda(counts, k=3.0)
    assert all(s.excess_fraction == 0.0 for s in states)
    assert all(s.lambda_daily == 0.0 for s in states) # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType, reportUnknownVariableType]
