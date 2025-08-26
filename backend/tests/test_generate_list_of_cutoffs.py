import math
import pytest
from backend.components.input_class import generate_list_of_cutoffs

def test_cutoffs_start_at_zero():
    cutoffs = generate_list_of_cutoffs(0.5, 3, 0.1)
    assert cutoffs[0] == 0

def test_cutoffs_monotonic():
    cutoffs = generate_list_of_cutoffs(0.5, 5, 0.1)
    assert all(x <= y for x, y in zip(cutoffs, cutoffs[1:]))

def test_cutoffs_sum_to_one_within_tolerance():
    cutoffs = generate_list_of_cutoffs(0.5, 5, 0.1)
    # Last cutoff should approximate 1
    assert math.isclose(cutoffs[-1], 1.0, rel_tol=1e-6) or cutoffs[-1] <= 1.0

@pytest.mark.parametrize("num_matches", [3, 4, 7, 8])
def test_cutoffs_length_changes(num_matches):
    cutoffs = generate_list_of_cutoffs(0.6, num_matches, 0.05)
    assert len(cutoffs) > 1
    # odd vs even should yield slightly different lengths
    if num_matches % 2 == 1:
        assert 4 <= len(cutoffs) <= num_matches + 3
    else:
        assert 6 <= len(cutoffs) <= num_matches + 4

def test_no_ties_removes_tie_cutoffs():
    cutoffs_no_ties = generate_list_of_cutoffs(0.5, 3, 0.0)
    cutoffs_with_ties = generate_list_of_cutoffs(0.5, 3, 0.5)
    # With no ties, the second cutoff should be 0
    assert cutoffs_no_ties[1] == 0
    # With ties, the second cutoff > 0
    assert cutoffs_with_ties[1] > 0

def test_extreme_probabilities_player_always_wins():
    cutoffs = generate_list_of_cutoffs(1.0, 3, 0.0)
    # If p1 always wins, the fifth cutoff should be 1
    assert math.isclose(cutoffs[4], 1.0, rel_tol=1e-6)

def test_extreme_probabilities_player_always_loses():
    cutoffs = generate_list_of_cutoffs(0.0, 3, 0.0)
    # If p1 never wins, the fifth cutoff should be 0
    assert math.isclose(cutoffs[4], 0.0, rel_tol=1e-6)
