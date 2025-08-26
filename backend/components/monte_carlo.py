from MTG-CALCULATOR-2.backend import InputData 
from .score_class import ScoreData
from .player_class import PlayerData, AllPlayerData
import random 
import math

def monte_carlo_simulation(data: InputData):
    # placeholder example
    top_9_outcomes = []
    top_8_outcomes = []
    for i in range(data.monteCarloIterations):
        game_instance=list(simulate_tourney(data).values())
        game_instance_ordered=order(game_instance,data.tiebreakers)
        top_9_outcomes.append(game_instance_ordered[data.targetTop])
        top_8_outcomes.append(game_instance_ordered[data.targetTop-1])
    out = process(top_9_outcomes, top_8_outcomes, data.tiebreakers,data.monteCarloIterations)
    return out 

def simulate_tourney(data: InputData):
    AllPlayerData_1=AllPlayerData(data)
    for i in range(data.numMatches):
        (pairs,bye)=set_pairings(AllPlayerData_1.DictPlayers,data)
        for j in pairs:
            simulate_match(j,AllPlayerData_1.DictPlayers,data)
        if bye != None:
            simulate_bye(bye,AllPlayerData_1.DictPlayers)
    AllPlayerData_1.Set_Scores()
    return AllPlayerData_1.DictPlayersScores

def simulate_match(j:tuple,players_dict,data:InputData):
    player_1=players_dict[j[0]]
    player_2=players_dict[j[1]]
    random_number=random.random()
    if player_1.Comp:
        if player_2.Comp:
            (player_1_outcome,player_2_outcome)=data.function_of_match_outcomes_comp(random_number)
        else:
            (player_1_outcome,player_2_outcome)=data.function_of_match_outcomes_mismatched(random_number)
    else:
        if player_2.Comp:
            (player_2_outcome,player_1_outcome)=data.function_of_match_outcomes_mismatched(random_number)
        else:
            (player_1_outcome,player_2_outcome)=data.function_of_match_outcomes_uncomp(random_number)
    if player_1_outcome[0]=='won':
        player_1.MatchesWon+=1
        player_2.MatchesLost+=1
    elif player_1_outcome[0]== 'lost':
        player_1.MatchesLost+=1
        player_2.MatchesWon+=1
    else:
        player_1.MatchesTied+=1
        player_2.MatchesTied+=1
        
    player_1.OpponentsPlayed.append(player_2.key)
    player_1.GamesWon+=player_1_outcome[1]
    player_1.GamesLost+=player_1_outcome[2]
    player_1.GamesTied+=player_1_outcome[3]
    
    player_2.OpponentsPlayed.append(player_1.key)
    player_2.GamesWon+=player_2_outcome[1]
    player_2.GamesLost+=player_2_outcome[2]
    player_2.GamesTied+=player_2_outcome[3]

def simulate_bye(bye: int,players_dict):
    player=players_dict[bye]
    player.MatchesWon+=1




def set_pairings(players_dict:dict, data : InputData ):
    players= list(players_dict.values())
    
    players.sort(key= lambda p: -1*p.get_points(data))
    
    keys=[]
    for i in players:
        keys.append(int(i.key))

    pairs= []
    bye=None

    while len(keys)>0:
        key1=keys[0]
        player1=players_dict[key1]
        keys.pop(0)
        if (len(keys)==0):
            bye=key1
        else:
            set_keys=set(keys)
            set_opponents=set(player1.OpponentsPlayed)
            set_new_opponent= set_keys-set_opponents
            if(len(set_new_opponent)>0):
                for i in keys:
                    if (i in set_new_opponent):
                        pairs.append((key1,i))
                        keys.remove(i)
                        break
            else: 
                pairs.append((key1,keys[0])) 
                keys.pop(0)
    return (pairs,bye)



def order(data: list[ScoreData], tiebreakers):
      # people.sort(key=lambda p: (p.age, p.height))
    if( tiebreakers[0]):
        if tiebreakers[1]:
            if tiebreakers[2]:
                data.sort(key= lambda p: (p.points,p.OMW,p.GW,p.OGW))
            else:
                data.sort(key= lambda p: (p.points,p.OMW,p.GW))
        elif tiebreakers[2]:
            data.sort(key= lambda p: (p.points,p.OMW,p.GW))
        else:
            data.sort(key= lambda p: (p.points,p.OMW))
    elif tiebreakers[1]:
        if tiebreakers[2]:
            data.sort(key= lambda p: (p.points,p.OGW,p.GW))
        else:
            data.sort(key= lambda p: (p.points,p.OGW))
    elif tiebreakers[2]:
        data.sort(key= lambda p: (p.points,p.GW))
    else:
        data.sort(key= lambda p: p.points)


    return data

def process( top_9: list, top_8:list , tiebreakers: list[bool],monte_carlo_iterations):
    #returns 
        # highest scores of number 9
        # lowest scores of number 8
        # median scores of number 8
    top_9_ordered= order(top_9, tiebreakers)
    top_8_ordered = order( top_8, tiebreakers)
    
    return (top_9_ordered[monte_carlo_iterations-1],top_9_ordered[int((monte_carlo_iterations-1)/2)],top_8_ordered[0],top_8_ordered[int((monte_carlo_iterations-1)/2)])
        
data = InputData(numPlayers=11,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=3, pointsPerTie=1, pointsPerLoss=0, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=0,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=True,monteCarloIterations=11)

monte_carlo_simulation(data)