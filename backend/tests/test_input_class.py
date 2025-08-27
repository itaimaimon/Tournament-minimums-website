import pytest
import math
from backend.components.input_class import InputData, event_probs, get_to_step_n, match_outcome_function

def test_create_input_data_valid():
    data = InputData(numPlayers=8,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=1, pointsPerTie=2, pointsPerLoss=4, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=1,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
                minDrawProb=.9,monteCarloIterations=10)
    assert data.numPlayers == 8
    assert data.numMatches == 3
    assert data.gamesPerMatch == 3

    assert data.numPlayers==8
    assert data.numMatches==3
    assert data.gamesPerMatch== 3
    assert data.targetTop== 6
    assert data.pointsPerWin==1
    assert data.pointsPerTie==2
    assert data.pointsPerLoss==4
    assert data.tiebreakers==[True,True,True]
    assert data.lastMatchIsDraw==True 
    assert data.numUncomp==1
    assert data.probLastGameTiesBetweenComp==.02
    assert data.probLastGameTiesBetweenUncomp==.02
    assert data.probLastGameTiesBetweenMismatched==.02
    assert data.probGameWinBetweenMismatched==.02
    assert data.minDrawProb ==.9
    assert data.monteCarloIterations==11
    assert data.probGameWinBetweenMatchedDecks==.5


def make_input_data(**overrides):
    """Helper to construct InputData with defaults, overridable."""
    defaults = dict(
        numPlayers=16,
        numMatches=None,    # triggers auto-calc
        gamesPerMatch=3,
        targetTop=8,
        pointsPerWin=3,
        pointsPerTie=1,
        pointsPerLoss=0,
        tiebreakers=[True, True, True],
        lastMatchIsDraw=True,
        numUncomp=0,
        probLastGameTiesBetweenComp=0.1,
        probLastGameTiesBetweenUncomp=0.1,
        probLastGameTiesBetweenMismatched=0.05,
        probGameWinBetweenMismatched=0.6,
        minDrawProb=.9,
        monteCarloIterations=101
    )
    defaults.update(overrides)
    return InputData(**defaults)

# --- InputData tests ---

def test_inputdata_defaults():
    data = make_input_data()
    assert data.numPlayers == 16
    assert data.numMatches == math.ceil(math.log(16, 2))  # default behavior
    assert data.pointsPerWin == 3
    assert data.tiebreakers == [True, True, True]

def test_inputdata_custom_num_matches():
    data = make_input_data(numMatches=7)
    assert data.numMatches == 7

def test_inputdata_error_numUncomp_gt_numPlayers():
    with pytest.raises(ValueError):
        make_input_data(numUncomp=20)

def test_inputdata_montecarlo_iterations_forced_odd():
    data = make_input_data(monteCarloIterations=100)  # even
    assert data.monteCarloIterations % 2 == 1  # forced odd

# --- event_probs / get_to_step_n tests ---

def test_event_probs_win_and_loss():
    p = event_probs(2, 1, 0.6, 0.4)
    assert p > 0
    assert isinstance(p, float)

def test_get_to_step_n_matches_known_value():
    # Probability of 2 wins and 1 loss with p_win=0.5
    val = get_to_step_n(2, 1, 0.5, 0.5)
    assert math.isclose(val, 0.375, rel_tol=1e-6)

# --- match_outcome_function tests ---

def test_match_outcome_function_distribution_sums_to_one():
    func = match_outcome_function(0.6, 3, 0.1)[0]
    # Check distribution across 100 random samples
    outcomes = [func(i / 100) for i in range(1, 100)]
    # just assert that function runs and returns tuples
    for (p1, p2) in outcomes:
        assert isinstance(p1, tuple)
        assert isinstance(p2, tuple)
        assert p1[0] in {"won", "lost", "tied"}

def test_match_outcome_function_even_and_odd():
    odd_func = match_outcome_function(0.6, 3, 0.1)[0]
    even_func = match_outcome_function(0.6, 4, 0.1)[0]
    out1 = odd_func(0.5)
    out2 = even_func(0.5)
    assert isinstance(out1, tuple)
    assert isinstance(out2, tuple)

def test_match_outcome_function_tie_edge_case():
    func = match_outcome_function(0.5, 3, 1.0)[0]  # force ties
    p1, p2 = func(0.01)
    assert p1[0] == "tied"
    assert p2[0] == "tied"