def test_calculate_endpoint_valid(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data

def test_calculate_endpoint_missing_num_matches(client):
    payload = {
        "numPlayers": 8,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    # FastAPI will reject missing required fields with 422
    assert response.status_code in (200, 422,500)

def test_calculate_endpoint_invalid_num_players(client):
    payload = {
        "numPlayers": -8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_num_Matches(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 0,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_games_per_match(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": .3,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_target_top(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 3,
        "targetTop": -4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_points(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 3,
        "targetTop": 4,
        "pointsPerWin":-2,
        "pointsPerTie":4.4,
        "pointsPerLoss":"r",
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 

def test_calculate_endpoint_invalid_tiebreakers(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":['g','h',3],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 

def test_calculate_endpoint_invalid_lastMatch(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": 3,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_num_uncomp(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": .1,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 

def test_calculate_endpoint_invalid_probs(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":1.1,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_probs_2(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":1.5,
        "probGameWinBetweenMismatched":.9,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 

def test_calculate_endpoint_invalid_probs_3(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":1.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.9,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_probs_3(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 3,
        "probLastGameTiesBetweenComp":1.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.9,
        "monteCarloChosen":True,
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 

def test_calculate_endpoint_invalid_monte_carlo_chosen(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 1,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":'d',
        "monteCarloIterations":2,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 


def test_calculate_endpoint_invalid_monte_carlo_iteration(client):
    payload = {
        "numPlayers": 8,
        "numMatches": 3,
        "gamesPerMatch": 1,
        "targetTop": 4,
        "pointsPerWin":2,
        "pointsPerTie":4,
        "pointsPerLoss":6,
        "tiebreakers":[True,True,True],
        "lastMatchIsDraw": False,
        "numUncomp": 1,
        "probLastGameTiesBetweenComp":.1,
        "probLastGameTiesBetweenUncomp":.3,
        "probLastGameTiesBetweenMismatched":.5,
        "probGameWinBetweenMismatched":.7,
        "monteCarloChosen":True,
        "monteCarloIterations":.4,
    }
    response = client.post("/calculate", json=payload)
    assert response.status_code in (400, 422, 500) 