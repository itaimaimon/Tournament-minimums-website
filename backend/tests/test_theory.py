import pytest
from backend.theory import calculate_minimum_results,InputData



def test_calculate_minimum_results_direct_calc_runs():
    data = InputData(numPlayers=8,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=1, pointsPerTie=2, pointsPerLoss=4, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=1,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)
    result = calculate_minimum_results(data)
    assert result is not None  # adjust when you know exact structure

def test_calculate_minimum_results_monte_carlo_runs():
    data = InputData(numPlayers=8,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=1, pointsPerTie=2, pointsPerLoss=4, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=1,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=True,monteCarloIterations=10)
    result = calculate_minimum_results(data)
    assert result is not None  # adjust when you know exact structure

