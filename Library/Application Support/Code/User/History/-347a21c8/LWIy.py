# tests/test_model.py
from giga_atom.simulations import compute_excess_and_lambda, baseline_counts

# Type hints for imported functions (for type checkers)
from typing import Callable, List, Any, Protocol

# Protocol for the expected state object
class StateLike(Protocol):
    excess_fraction: float
    lambda_daily: float

compute_excess_and_lambda: Callable[[Any, float], List[StateLike]]
baseline_counts: Callable[[], list]

def test_baseline_no_excess():
    counts = baseline_counts()
    states: List[StateLike] = compute_excess_and_lambda(counts, k=3.0)
    from typing import cast
    assert all(cast(StateLike, s).excess_fraction == 0.0 for s in states)
    assert all(cast(StateLike, s).lambda_daily == 0.0 for s in states)
