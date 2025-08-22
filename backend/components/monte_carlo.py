from .input_class import InputData 
from .score_class import ScoreData
from .player_class import PlayerData, AllPlayerData

def monte_carlo_simulation(data: InputData):
    # placeholder example
    top_9_outcomes = []
    top_8_outcomes = []
    for i in range(1001):
        game_instance=simulate_tourney(data)
        top_9_outcomes.append(game_instance[data.targetTop])
        top_8_outcomes.append(game_instance[data.targetTop-1])
    out = process(top_9_outcomes, top_8_outcomes, data.tiebreakers)
    return out 

def simulate_tourney(data: InputData):
    AllPlayerData_1=AllPlayerData(data)
    for i in range(data.numMatches):
        (pairs,bye)=set_pairings(AllPlayerData_1.DictPlayers,data)
        

    return 0


def set_pairings(players_dict:dict, data : InputData ):
    players= list(players_dict.values())
    
    players.sort(key= lambda p: -1*p.get_points(data))
    
    keys=[]
    for i in players:
        keys.append(i.key)

    pairs= []
    bye=None

    while len(players)>0:
        player1=players[0]
        key1=keys[0]
        players.pop(0)
        keys.pop(0)
        if (len(players)==0):
            bye=players[0]
        else:
            set_keys=set(keys)
            set_opponents=set(player1.OpponentsPlayed)
            set_new_opponent= set_keys-set_opponents
            if(len(set_new_opponent)>0):
                for i in keys:
                    if (i in set_new_opponent):
                        pairs.append((key1,i))
                        keys.remove(i)
                        players.remove(players_dict[i])
                        break
            else: 
                pairs.append((key1,keys[0])) 
                players.pop(0)
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

def process( top_9: list, top_8:list , tiebreakers: list[bool]):
    #returns 
        # highest scores of number 9
        # lowest scores of number 8
        # median scores of number 8
    top_9_ordered= order(top_9, tiebreakers)
    top_8_ordered = order( top_8, tiebreakers)
    return (top_9_ordered[1000],top_9_ordered[500],top_8_ordered[0],top_8_ordered[500])
