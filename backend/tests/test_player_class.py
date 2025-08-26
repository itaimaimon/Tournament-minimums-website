import pytest
from backend.components.player_class import PlayerData, AllPlayerData  # adjust import to your module path
from backend.components.input_class import InputData
from backend.components.score_class import ScoreData

def test_playerdata_get_points_win_loss_tie():
    data = InputData(numPlayers=8,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=3, pointsPerTie=1, pointsPerLoss=0, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=1,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)
    player = PlayerData(
        key=0, Comp=True,
        MatchesWon=2, MatchesLost=1, MatchesTied=1,
        OpponentsPlayed=[], GamesWon=0, GamesLost=0, GamesTied=0
    )
    assert player.get_points(data) == 2*3 + 1*0 + 1*1  # 7 points


def test_allplayerdata_initialization_creates_players(monkeypatch):
    data = InputData(numPlayers=5,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=3, pointsPerTie=1, pointsPerLoss=0, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=2,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)
    # Patch random.sample to make test deterministic
    monkeypatch.setattr("backend.components.player_class.random.sample", lambda x, n: [0, 2])

    apd = AllPlayerData(data)
    assert len(apd.DictPlayers) == 5
    assert set(apd.Uncomp) == {0, 2}
    assert all(isinstance(p.Score, ScoreData) for p in apd.DictPlayers.values())


def test_set_scores_computes_correct_values():
    data = InputData(numPlayers=2,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=3, pointsPerTie=1, pointsPerLoss=0, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=0,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)
    apd = AllPlayerData(data)

    # Set up matches manually
    p0 = apd.DictPlayers[0]
    p1 = apd.DictPlayers[1]

    # Player 0 beat player 1
    p0.MatchesWon = 1
    p0.OpponentsPlayed = [1]
    p0.GamesWon = 2
    p0.GamesLost = 0
    p0.GamesTied = 0

    p1.MatchesLost = 1
    p1.OpponentsPlayed = [0]
    p1.GamesWon = 0
    p1.GamesLost = 2
    p1.GamesTied = 0

    apd.Set_Scores()

    # Check p0 score
    score0 = apd.DictPlayers[0].Score
    assert pytest.approx(score0.points) == 3   # one win
    assert pytest.approx(score0.GW, rel=1e-6) == 1.0  # 2/2
    assert 0 <= score0.OMW <= 1
    assert 0 <= score0.OGW <= 1

    # Check p1 score
    score1 = apd.DictPlayers[1].Score
    assert pytest.approx(score1.points) == 0   # one loss
    assert pytest.approx(score1.GW, rel=1e-6) == 0.0  # 0/2


def test_set_scores_no_opponents_does_nothing():
    data =     data = InputData(numPlayers=1,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=1, pointsPerTie=2, pointsPerLoss=4, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=0,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)
    apd = AllPlayerData(data)
    # No opponents, so Set_Scores should skip
    apd.Set_Scores()
    assert isinstance(apd.DictPlayers[0].Score, ScoreData)
