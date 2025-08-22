from components.input_class import InputData
from components.monte_carlo import monte_carlo_simulation
from components.direct_calc import direct_calculation
from components.utils import format_result_direct_calc, format_result_monte_carlo
from components.score_class import ScoreData

def calculate_minimum_results(data: InputData) -> str:
    # Choose one calculation method
    # Example: pick Monte Carlo if roundsPlayed > 5

    if (data.targetTop>=data.numPlayers):
        score=ScoreData(
            points=0,
            OMW=0,
            GW=0,
            OGW=0
        )
        return format_result_direct_calc(score,data.tiebreakers, data.targetTop) 
    elif data.monteCarloChosen:
        output_list = monte_carlo_simulation(data)
        return format_result_monte_carlo(output_list[0],output_list[1],output_list[2],output_list[3], data.tiebreakers, data.targetTop)
    else:
        output = direct_calculation(data)
        return format_result_direct_calc(output, data.tiebreakers, data.targetTop)