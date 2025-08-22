from .score_class import ScoreData

# Example constants or small helper functions
def format_result(data: ScoreData, tiebreakers: list[bool]):
    points_needed=data.points
    OMW=data.OMW
    GW=data.GW
    OGW=data.OGW

    OMW_chosen=tiebreakers[0]
    GW_chosen=tiebreakers[1]
    OGW_chosen=tiebreakers[2]

    start_string= f"{points_needed} wins"
    OMW_string= f"an opponenet match win rate of {OMW}"
    GW_string= f"a game win rate of {GW}"
    OGW_string= f"an opponenet game win rate of {OGW}"

    full_string = start_string
    if OMW_chosen:
        if not GW_chosen and not OGW_chosen:
            return full_string + ", and " + OMW_string
        else:
            full_string += ", " + OMW_string

        if GW_chosen:
            if OGW_chosen:
                return full_string + ", " + GW_string +", and " + OGW_string
            else:
                return full_string + ", and " + GW_string
        elif OGW_chosen:
            return full_string + ", and " + OGW_string

    elif GW_chosen:
        if OGW_chosen:
            return full_string + ", " + GW_string +", and " + OGW_string
        else:
            return full_string + ", and " + GW_string
    elif OGW_chosen:
        return full_string + ", and " + OGW_string
    else:
        return full_string
    
def format_result_direct_calc(data: ScoreData, tiebreakers: list[bool], top: int):
    out_string= "We estimate that you need at least" + format_result(data, tiebreakers) + f" to make top {top}" 
    return out_string

def format_result_monte_carlo(data_best_ninth_place: ScoreData, data_med_ninth_place:ScoreData, data_worst_eighth_place:ScoreData, data_med_eighth_place:ScoreData, tiebreakers: list[bool], top: int):
    start_string= "The result of 1001 simulations is that"
    second_string= f" the best score at place {top+1} was " + format_result(data_best_ninth_place,tiebreakers)
    third_string = f". The median score at place {top+1} was " + format_result(data_med_ninth_place)
    third_string = f". The worst score at place {top} was " + format_result(data_worst_eighth_place)
    last_string = f". The median score at place {top} was " + format_result(data_med_eighth_place) + "."