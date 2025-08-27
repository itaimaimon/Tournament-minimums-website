# tests/test_simulation.py
import pytest
import random
from unittest.mock import patch, MagicMock
from backend.components.player_class import PlayerData, AllPlayerData, ScoreData

# Import functions to test
from backend.components.monte_carlo import (
    monte_carlo_simulation,
    simulate_tourney,
    simulate_match,
    simulate_bye,
    set_pairings,
    order,
    process,
)

# ---- Fixtures ----
class DummyPlayer:
    def __init__(self, key, comp=False):
        self.key = key
        self.Comp = comp
        self.MatchesWon = 0
        self.MatchesLost = 0
        self.MatchesTied = 0
        self.GamesWon = 0
        self.GamesLost = 0
        self.GamesTied = 0
        self.OpponentsPlayed = []

    def get_points(self, data):
        return self.MatchesWon * 3 + self.MatchesTied




class DummyInput:
    def __init__(self):
        self.numMatches = 2
        self.targetTop = 1
        self.tiebreakers = [True, True, True]
        self.monteCarloIterations = 2
        self.funcMatchOutcomesComp = lambda r: (("won", 2, 0, 0), ("lost", 0, 2, 0))
        self.funcMatchOutcomesMismatched = lambda r: (("won", 2, 0, 0), ("lost", 0, 2, 0))
        self.funcMatchOutcomesUncomp = lambda r: (("tied", 1, 1, 1), ("tied", 1, 1, 1))
        self.lastMatchIsDraw = False
        self.minDrawProb = 0.9
        self.gamesPerMatch = 3

class DummyScore:
    def __init__(self, points=0, OMW=0, GW=0, OGW=0):
        self.points = points
        self.OMW = OMW
        self.GW = GW
        self.OGW = OGW


# ---- Tests ----

def test_simulate_match_updates_players():
    p1 = DummyPlayer("A", comp=True)
    p2 = DummyPlayer("B", comp=True)
    players = {"A": p1, "B": p2}
    data = DummyInput()

    with patch("random.random", return_value=0.5):
        simulate_match(("A", "B"), players, data)

    assert p1.MatchesWon + p1.MatchesLost + p1.MatchesTied > 0
    assert p2.MatchesWon + p2.MatchesLost + p2.MatchesTied > 0


def test_simulate_bye_gives_win():
    p = DummyPlayer("A")
    players = {"A": p}
    simulate_bye("A", players)
    assert p.MatchesWon == 1


def test_set_pairings_even_players():
    players = {i: DummyPlayer(str(i)) for i in range(4)}
    data = DummyInput()
    pairs, bye = set_pairings(players, data)
    assert len(pairs) == 2
    assert bye is None


def test_set_pairings_with_bye():
    players = {i: DummyPlayer(str(i)) for i in range(3)}
    data = DummyInput()
    pairs, bye = set_pairings(players, data)
    assert len(pairs) >= 1
    # bye should be one of the players
    assert isinstance(bye, int)


def test_ordering_respects_tiebreakers():
    scores = [
        DummyScore(points=3, OMW=3, GW=1, OGW=0),
        DummyScore(points=3, OMW=2, GW=2, OGW=1),
    ]
    result = order(scores, [True, True, True])
    assert result[0].OMW > result[1].OMW


def test_process_returns_expected_tuple():
    scores = [DummyScore(points=i) for i in range(5)]
    result = process(scores, scores, [True, True, True], len(scores))
    assert isinstance(result, tuple)
    assert len(result) == 4


def test_simulate_tourney_runs(monkeypatch):
    data = DummyInput()

    class DummyAllPlayers:
        def __init__(self, data):
            self.DictPlayers = {0: DummyPlayer("A"), 1: DummyPlayer("B")}
            self.DictPlayersScores = {0: DummyScore(), 1: DummyScore()}

        def Set_Scores(self):
            pass

    monkeypatch.setattr("backend.components.monte_carlo.AllPlayerData", DummyAllPlayers)
    monkeypatch.setattr("backend.components.monte_carlo.set_pairings", lambda d, _: ([(0, 1)], None))
    monkeypatch.setattr("backend.components.monte_carlo.simulate_match", lambda j, d, data: None)

    scores = simulate_tourney(data)
    assert isinstance(scores, dict)


def test_monte_carlo_simulation_runs(monkeypatch):
    data = DummyInput()

    monkeypatch.setattr("backend.components.monte_carlo.simulate_tourney", lambda d: {0: DummyScore(points=5), 1: DummyScore(points=2)})
    monkeypatch.setattr("backend.components.monte_carlo.order", lambda l, t: l)
    monkeypatch.setattr("backend.components.monte_carlo.process", lambda a, b, c, d: ("ok", "median", "low", "mid"))

    result = monte_carlo_simulation(data)
    assert result[0] == "ok"
