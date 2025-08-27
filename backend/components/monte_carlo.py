from backend.components.input_class import InputData 
from backend.components.score_class import ScoreData
from backend.components.player_class import PlayerData, AllPlayerData
import random 
import math
import copy



def monte_carlo_simulation(data: InputData):
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
        if bye != None:
            simulate_bye(bye,AllPlayerData_1.DictPlayers)
        if i<data.numMatches-1 or not data.lastMatchIsDraw:
            for j in pairs:
                simulate_match(j,AllPlayerData_1.DictPlayers,data)
        else:
            drawers= determine_draw(pairs,AllPlayerData_1,data)
            for j in pairs:
                if j in drawers:
                    player_1=AllPlayerData_1.DictPlayers[j[0]]
                    player_2=AllPlayerData_1.DictPlayers[j[1]]

                    player_1.MatchesTied+=1
                    player_2.MatchesTied+=1
                    player_1.OpponentsPlayed.append(player_2.key)
                    player_2.OpponentsPlayed.append(player_1.key)
                    player_1.GamesTied+=data.gamesPerMatch
                    player_2.GamesTied+=data.gamesPerMatch
                else:
                    simulate_match(j,AllPlayerData_1.DictPlayers,data)
    AllPlayerData_1.Set_Scores()
    return AllPlayerData_1.DictPlayersScores

def determine_draw(pairs,AllPlayerData_1: AllPlayerData, data:InputData):
    minDrawProp = data.minDrawProb*50
    if minDrawProp-math.floor(minDrawProp)>.5:
        minDrawProp=math.ceil(minDrawProp)
    else:
        minDrawProp=math.floor(minDrawProp)

    num_losses_1=[50-minDrawProp]*len(pairs)
    num_losses_2=[50-minDrawProp]*len(pairs)
    for i in range(50):
        AllPlayerData_i=copy.deepcopy(AllPlayerData_1)
        for i in pairs:
            simulate_match(i,AllPlayerData_i.DictPlayers,data)
        
        AllPlayerData_i.Set_Scores()    
        for keyj in range(len(pairs)):
            j=pairs[keyj]
            player_1_new=AllPlayerData_i.DictPlayers[j[0]]
            player_2_new=AllPlayerData_i.DictPlayers[j[1]]
            player_1_old=copy.deepcopy(AllPlayerData_1.DictPlayers[j[0]])
            player_2_old=copy.deepcopy(AllPlayerData_1.DictPlayers[j[1]])
            AllPlayerData_i.DictPlayers[j[0]]=player_1_old
            AllPlayerData_i.DictPlayers[j[1]]=player_2_old
    
            player_1_old.MatchesTied+=1
            player_2_old.MatchesTied+=1
            player_1_old.OpponentsPlayed.append(player_2_old.key)
            player_2_old.OpponentsPlayed.append(player_1_old.key)
            player_1_old.GamesTied+=data.gamesPerMatch
            player_2_old.GamesTied+=data.gamesPerMatch
            AllPlayerData_i.Set_Score_i(player_1_old.key)
            AllPlayerData_i.Set_Score_i(player_2_old.key)
    
            scores_list=list(AllPlayerData_i.DictPlayersScores.values())
            ordered_scores=order(scores_list,data.tiebreakers)
            place_1= ordered_scores.index(player_1_old.Score)+1
            place_2= ordered_scores.index(player_2_old.Score)+1
            if place_1>data.targetTop:
                num_losses_1[keyj]-=1
            if place_2>data.targetTop:
                num_losses_2[keyj]-=1
            AllPlayerData_i.DictPlayers[j[0]]=player_1_new
            AllPlayerData_i.DictPlayers[j[1]]=player_2_new

    drawers=[]
    for j in range(len(pairs)):
        if num_losses_1[j]>0 and num_losses_2[j]>0:
            drawers.append(pairs[j])

    return drawers

def simulate_match(j:tuple,players_dict,data:InputData):
    player_1=players_dict[j[0]]
    player_2=players_dict[j[1]]
    random_number=random.random()
    if player_1.Comp:
        if player_2.Comp:
            (player_1_outcome,player_2_outcome)=data.funcMatchOutcomesComp(random_number)
        else:
            (player_1_outcome,player_2_outcome)=data.funcMatchOutcomesMismatched(random_number)
    else:
        if player_2.Comp:
            (player_2_outcome,player_1_outcome)=data.funcMatchOutcomesMismatched(random_number)
        else:
            (player_1_outcome,player_2_outcome)=data.funcMatchOutcomesUncomp(random_number)
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
    
    players.sort(key= lambda p: p.get_points(data),reverse=True)
    
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



def order(data: list, tiebreakers: list[bool]):
    key_parts = [("points",)]
    if tiebreakers[0]:
        key_parts.append(("OMW",))
    if tiebreakers[1]:
        key_parts.append(("GW",))
    if tiebreakers[2]:
        key_parts.append(("OGW",))

    def sort_key(p):
        return tuple(getattr(p, part[0]) for part in key_parts)
    data.sort(key=sort_key, reverse=True)
    return data

def process( top_9: list, top_8:list , tiebreakers: list[bool],monte_carlo_iterations):
    #returns 
        # highest scores of number 9
        # lowest scores of number 8
        # median scores of number 8
    top_9_ordered= order(top_9, tiebreakers)
    top_8_ordered = order( top_8, tiebreakers)
    
    return (top_9_ordered[0],top_9_ordered[int((monte_carlo_iterations-1)/2)],top_8_ordered[int(monte_carlo_iterations-1)],top_8_ordered[int((monte_carlo_iterations-1)/2)])
