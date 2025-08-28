from backend.components.score_class import ScoreData
from backend.components.input_class import InputData
import math
from backend.components.player_class import PlayerData, AllPlayerData
from backend.components.input_class import generate_list_of_cutoffs





testdata = InputData(numPlayers=8,numMatches=3, gamesPerMatch=3, targetTop=6, pointsPerWin=3, pointsPerTie=1, pointsPerLoss=0, tiebreakers=[True,True,True], lastMatchIsDraw=True, 
        numUncomp=1,probLastGameTiesBetweenComp=.02, probLastGameTiesBetweenUncomp=.02,probLastGameTiesBetweenMismatched=.02,probGameWinBetweenMismatched=.02,
        monteCarloChosen=False,monteCarloIterations=10)



def direct_calculation(data: InputData):
    # placeholder example
    full_dictionary_of_all_scores_as_dict_of_dict=full_proportion_of_all_scores(data)
    full_dictionary_of_all_scores=dictionary_of_dictionary_to_dictionary_input_tuples(full_proportion_of_all_scores(data))

    return ScoreData(points=0, OMW=0, GW=0, OGW=0)





def proportion_of_all_scores(data: InputData):
    #output is a dictionary
    #dictionary takes in point value and outputs list of tuples where each tuple is of form 
    #(number of wins, number of ties, number of losses, ways this could have happened in the given match number)
    # and each tuple results in the given point value
    out={}
    
    points_per_win=data.pointsPerWin
    points_per_loss=data.pointsPerLoss
    points_per_tie=data.pointsPerTie
    matches_for_func=data.numMatches


    for num_wins in range(0,matches_for_func+1):
        for num_ties in range(0,matches_for_func-num_wins+1):
            num_losses=matches_for_func-num_wins-num_ties
            points=num_wins*points_per_win+num_losses*points_per_loss+num_ties*points_per_tie
            ways_to_get_this= math.factorial(matches_for_func)/(math.factorial(num_losses)*math.factorial(num_wins)*math.factorial(num_ties))
            if points in out:
                oldlist=out.get(points)
                oldlist.append((num_wins,num_ties,num_losses,ways_to_get_this))
                out[points]=oldlist
            else:
                out[points]=[(num_wins,num_ties,num_losses,ways_to_get_this)]
    return out  


def dictionary_of_dictionary_to_dictionary_input_tuples(mydict,recursion=0):
    out={}
    keys1=mydict.keys()
    for i in keys1:
        nextdict=mydict[i]
        keys2=nextdict.keys()
        for j in keys2:
            if recursion==0:
                out[(i,j)]=nextdict[j]
            else:
                ij=i+(j)
                out[ij]=nextdict[j]
    return out

def test_dict_of_dict():
    proportions = dictionary_of_dictionary_to_dictionary_input_tuples({(1,2):{1:1,2:2},(2,3):{3:1}},recursion=1)
    # Last cutoff should approximate 1
    assert proportions.keys().sort() == [(1,2,1),(1,2,2),(2,3,3)]

def full_proportion_of_all_scores(data: InputData):
    matches=data.numMatches
    out={}
    for i in range(matches):
        out[i]=proportion_of_all_scores(i)
    return out        



def expected_outcome_of_rand_round(data:InputData,number_of_comp_decks,number_of_uncomp_decks,proportion_of_comp_decks,proportion_of_uncomp_decks):
    probability_of_match_ties_between_comp_decks=data.probability_of_match_ties_between_comp_decks
    probability_of_match_ties_between_uncomp_decks=data.probability_of_match_ties_between_uncomp_decks
    probability_of_match_ties_between_mismatched_decks=data.probability_of_match_ties_between_mismatched_decks
    probability_of_match_win_between_mismatched_decks=data.probability_of_match_win_between_mismatched_decks
            
    #output is tuple of expected number of compettive decks that won, expected number of uncompettive decks that lost, expected number of uncompettitive decks that tied,
    #expected number of non-compettive decks that won, expected number of non-compettive decks that tied, expected number of noncompettive decks that lost

    comp_wins=number_of_comp_decks*(proportion_of_comp_decks*(1-probability_of_match_ties_between_comp_decks)/2+proportion_of_uncomp_decks*probability_of_match_win_between_mismatched_decks)
    comp_ties=number_of_comp_decks*(proportion_of_comp_decks*(probability_of_match_ties_between_comp_decks)+proportion_of_uncomp_decks*probability_of_match_ties_between_mismatched_decks)
    comp_loss=number_of_comp_decks*(proportion_of_comp_decks*(1-probability_of_match_ties_between_comp_decks)/2+proportion_of_uncomp_decks*(1-probability_of_match_win_between_mismatched_decks-probability_of_match_ties_between_mismatched_decks))

    un_comp_wins=number_of_uncomp_decks*(proportion_of_uncomp_decks*(1-probability_of_match_ties_between_uncomp_decks)/2+proportion_of_comp_decks*(1-probability_of_match_win_between_mismatched_decks-probability_of_match_ties_between_mismatched_decks))
    un_comp_ties=number_of_uncomp_decks*(proportion_of_uncomp_decks*(probability_of_match_ties_between_uncomp_decks)+proportion_of_comp_decks*probability_of_match_ties_between_mismatched_decks)
    un_comp_loss=number_of_uncomp_decks*(proportion_of_uncomp_decks*(1-probability_of_match_ties_between_uncomp_decks)/2+proportion_of_comp_decks*(probability_of_match_win_between_mismatched_decks))

    return (comp_wins,comp_ties,comp_loss,un_comp_wins,un_comp_ties,un_comp_loss)

#outputs reasonable compettition range for all players with given score
def region_to_get_minimum_compettition(mydict,cutoff):
    scores=list(mydict.keys())
    scores.sort()
    out=[]
    bottom_range= []
    top_range = []
    for i in range(len(scores)):
        expected_players_at_i=mydict[scores[i]]
        outcome= expected_players_at_i[0]+expected_players_at_i[1]
        bottom_range_for_i=i
        top_range_for_i=i
        while outcome<cutoff and (bottom_range_for_i>=1 or top_range_for_i<=len(scores)-2):
            
            if bottom_range_for_i>=1:
                bottom_range_for_i+=-1
                outcome+=mydict[scores[bottom_range_for_i]][0]+mydict[scores[bottom_range_for_i]][1]
            if top_range_for_i<=len(scores)-2:
                top_range_for_i+=1
                outcome+=mydict[scores[top_range_for_i]][0]+mydict[scores[top_range_for_i]][1]
            
        bottom_range.append(bottom_range_for_i)
        top_range.append(top_range_for_i)
    for i in range(len(scores)):
        bottom_range_i=bottom_range[i]
        top_range_i=top_range[i]
        for j in range(len(scores)):
            if top_range[j]>=i and j<bottom_range_i:
                bottom_range_i=j
            if bottom_range[j]<=i and j> top_range_i:
                top_range_i=j
        bottom_range[i]=bottom_range_i
        top_range[i]=top_range_i
        out.append(list(range(bottom_range_i,top_range_i+1)))
    return out        


def Proportion_of_comp_v_noncomp_decks_with_certain_score(matches_so_far, data: InputData, full_dictionary_of_all_scores_as_dict_of_dict:dict):

    players=data.numPlayers
    number_of_uncomp_decks=data.numUncomp
    match_func=matches_so_far
    points_per_win=data.pointsPerWin
    points_per_loss=data.pointsPerLoss
    points_per_tie=data.pointsPerTie


    #output is a dictionary
    #dictionary takes in matches done so far and outputs dictionary that takes in certain acheivable score and outputs tuple
    # (aprox number of comp decks with given score, aprox number of non-comp decks with given score)
    #make corresponding dictionary taking in tuples after for cleanliness


    #start with dictonary of dictionary for ease and adjust at end
    out={0:{0:(players-number_of_uncomp_decks,number_of_uncomp_decks)}}

    for i in range(1,match_func+1):
        prev_possible_scores=list(full_dictionary_of_all_scores_as_dict_of_dict[i-1].keys())
        prev_possible_scores.sort()
        dict_match_i={}
        prev_dict=out[i-1]
        adjacent_scores_to_get_4=region_to_get_minimum_compettition(prev_dict,4)

        for j in range(len(prev_possible_scores)):
            curr_score=prev_possible_scores[j]
            expected_tuple=prev_dict[curr_score]
            total_comp=0
            total_uncomp=0
            for k in adjacent_scores_to_get_4[j]:
                range_expected_tuple_k=prev_dict[prev_possible_scores[k]]
                total_comp+=range_expected_tuple_k[0]
                total_uncomp+=range_expected_tuple_k[1]
            total_players_this_level=total_comp+total_uncomp
            comp_proportion=total_comp/total_players_this_level
            uncomp_proportion=total_uncomp/total_players_this_level
            outcomes= expected_outcome_of_rand_round(data,expected_tuple[0],expected_tuple[1], comp_proportion,uncomp_proportion)
            possible_scores_so_far=dict_match_i.keys()
            if curr_score+points_per_loss in possible_scores_so_far:
                prev=dict_match_i[curr_score+points_per_loss]
                new=(prev[0]+outcomes[2],prev[1]+outcomes[5])
                dict_match_i[curr_score+points_per_loss]=new
            else:   
                dict_match_i[curr_score+points_per_loss] =(outcomes[2],outcomes[5])
            
            if j+points_per_tie in possible_scores_so_far:
                prev=dict_match_i[curr_score+points_per_tie]
                new=(prev[0]+outcomes[1],prev[1]+outcomes[4])
                dict_match_i[curr_score+points_per_tie]=new
            else:
                dict_match_i[curr_score+points_per_tie]=(outcomes[1],outcomes[4])             
            
            if j+points_per_win in possible_scores_so_far:
                prev=dict_match_i[curr_score+points_per_win]
                new=(prev[0]+outcomes[0],prev[1]+outcomes[3])
                dict_match_i[curr_score+points_per_win]=new
            else:
                dict_match_i[curr_score+points_per_win] =(outcomes[0],outcomes[3])
        
        out[i]=dict_match_i
    return out



def find_proportions(dict_of_points_and_proportions):
    scores=list(dict_of_points_and_proportions.keys())
    scores.sort()
    summed_proportions={}
    running_total=0
    for i in scores:
        summed_proportions[i]=running_total
        running_total+=dict_of_points_and_proportions[i][0]+dict_of_points_and_proportions[i][1]
    return summed_proportions



def last_match_is_weird_cuttoff(dict_of_points_and_proportions):
    summed_proportions=find_proportions(dict_of_points_and_proportions)
    proportion_of_winners= players/winning_group
    scores=list(summed_proportions.keys())
    scores.sort()
    for i in scores:
        amount_to_be_subtracted=0
        if i-1 in summed_proportions.keys():
            amount_to_be_subtracted+=summed_proportions[i-1]
        if i-2 in summed_proportions.keys():
            amount_to_be_subtracted+=summed_proportions[i-2]
        if summed_proportions[i]-amount_to_be_subtracted>=winning_group:
            return i
    return (max(scores)+1)



def round_with_drawers(prev_dict):
    drawers_cutoff=last_match_is_weird_cuttoff(prev_dict)

    adjacent_scores_to_get_4=region_to_get_minimum_compettition(prev_dict,4)
    dict_match_i={}
    prev_possible_scores=list(prev_dict.keys())
    prev_possible_scores.sort()
    for j in range(len(prev_possible_scores)):
        curr_score=prev_possible_scores[j]
        expected_tuple=prev_dict[curr_score]
        total_comp=0
        total_uncomp=0
        for k in adjacent_scores_to_get_4[j]:
            range_expected_tuple_k=prev_dict[prev_possible_scores[k]]
            total_comp+=range_expected_tuple_k[0]
            total_uncomp+=range_expected_tuple_k[1]
        total_players_this_level=total_comp+total_uncomp
        comp_proportion=total_comp/total_players_this_level
        uncomp_proportion=total_uncomp/total_players_this_level
        if curr_score >=drawers_cutoff:
            outcomes = (0,expected_tuple[0],0,0,expected_tuple[1],0)
        else:
            outcomes= expected_outcome_of_round(expected_tuple[0],expected_tuple[1], comp_proportion,uncomp_proportion)
        possible_scores_so_far=dict_match_i.keys()
        if curr_score+points_per_loss in possible_scores_so_far:
            prev=dict_match_i[curr_score+points_per_loss]
            new=(prev[0]+outcomes[2],prev[1]+outcomes[5])
            dict_match_i[curr_score+points_per_loss]=new
        else:   
            dict_match_i[curr_score+points_per_loss] =(outcomes[2],outcomes[5])
            
        if j+points_per_tie in possible_scores_so_far:
            prev=dict_match_i[curr_score+points_per_tie]
            new=(prev[0]+outcomes[1],prev[1]+outcomes[4])
            dict_match_i[curr_score+points_per_tie]=new
        else:
            dict_match_i[curr_score+points_per_tie]=(outcomes[1],outcomes[4])             
            
        if j+points_per_win in possible_scores_so_far:
            prev=dict_match_i[curr_score+points_per_win]
            new=(prev[0]+outcomes[0],prev[1]+outcomes[3])
            dict_match_i[curr_score+points_per_win]=new
        else:
            dict_match_i[curr_score+points_per_win] =(outcomes[0],outcomes[3])
    return dict_match_i


def naive_distribution_of_scores(probability_of_winning_losing,matches):
    prob_distribution_of_opponent_scores_without_you={}
    oppo_possibilities=full_dictionary_of_all_scores_as_dict_of_dict[matches]
    oppo_scores=list(oppo_possibilities.keys())
    oppo_scores.sort()
    for i in oppo_scores:
        prob_distribution_of_opponent_scores_without_you[i]=0 
        for j in oppo_possibilities[i]:
            prob_distribution_of_opponent_scores_without_you[i]+=j[3]*probability_of_winning_losing**(j[0]+j[2])*(1-probability_of_winning_losing)**(j[1])
    return prob_distribution_of_opponent_scores_without_you



def add_probability_distributions(prob_distribution_1,prob_distribution_2):
    out={}
    keys1=prob_distribution_1.keys()
    keys2=prob_distribution_2.keys()
    for i in keys1:
        for j in keys2:
            if i.is_tuple() and j.is_tuple():
                k=tuple(np.add(i, j))
            else:
                k=i+j
            if k in out:
                out[k]+= prob_distribution_1[i]*prob_distribution_2[j]
            else:
                out[k]=prob_distribution_1[i]*prob_distribution_2[j]
    return out


def opponent_match_win_prop(score,players_beat):
    ways_to_get_score=full_dictionary_of_all_scores[(matches,score)]
    opponent_scores_from_you={}
    proportion_of_comp_decks=(players-number_of_uncomp_decks)/players
    proportion_of_uncomp_decks=number_of_uncomp_decks/players
    general_prob_of_winning_or_losing= (1/2)*proportion_of_comp_decks^2*(1-probability_of_match_ties_between_comp_decks)+proportion_of_uncomp_decks^2*(1-probability_of_match_ties_between_comp_decks)+2*proportion_of_comp_decks*proportion_of_uncomp_decks*(1-probability_of_match_ties_between_mismatched_decks)

    for i in ways_to_get_score:
        if 0*i[0]+1*i[1]+3*i[2] in opponent_scores_from_you.keys():
            opponent_scores_from_you[0*i[0]+1*i[1]+3*i[2]]=i[3]*general_prob_of_winning_or_losing**(i[0]+i[2])*(1-general_prob_of_winning_or_losing)**(i[1])
        else:
            opponent_scores_from_you[0*i[0]+1*i[1]+3*i[2]]+=i[3]*general_prob_of_winning_or_losing**(i[0]+i[2])*(1-general_prob_of_winning_or_losing)**(i[1])

    prob_distribution_of_opponent_scores_without_you=naive_distribution_of_scores(general_prob_of_winning_or_losing,matches-1)

    prob_distribution_to_consider=prob_distribution_of_opponent_scores_without_you.copy()
    for i in range(matches-2):
        prob_distribution_to_consider=add_probability_distributions(prob_distribution_to_consider,prob_distribution_of_opponent_scores_without_you)
    prob_distribution_to_consider=add_probability_distributions(prob_distribution_to_consider,opponent_scores_from_you)


    cut_off=(players-winning_group-players_beat)
    scores_of_others=list(prob_distribution_to_consider.keys())
    scores_of_others.sort()
    running_sum=0
    for i in range(len(scores_of_others)):
        if running_sum<=cut_off and running_sum+prob_distribution_to_consider[scores_of_others[i]]>cut_off:
            out1=scores_of_others[i]
            if i+1 < len(scores_of_others):
                out2=scores_of_others[i+1]
                running_sum_2=running_sum+prob_distribution_to_consider[scores_of_others[i+1]]
            else:
                out2=False
                running_sum_2=0
            cut_off-=running_sum
            break
        running_sum+=prob_distribution_to_consider[scores_of_others[i]]
    return (out1,running_sum,out2,running_sum_2)



def combine_distributions(prob_distribution_1,prob_distribution_2):
    out=prob_distribution_1.copy()
    keys1=prob_distribution_1.keys()
    keys2=prob_distribution_2.keys()
    for j in keys2:
        if j in keys1:
            out[j]+= prob_distribution_2[j]
        else:
            out[j]=prob_distribution_2[j]
    return out



def game_win_prop(score,score_cutoff_data,players_beat):
    ways_to_get_score=full_dictionary_of_all_scores[(matches,score)]

    num_comp_this_level=score_cutoff_data[score][0]
    num_uncomp_this_level=score_cutoff_data[score][1]

    prop_comp=(players-number_of_uncomp_decks)/players
    prop_uncomp=number_of_uncomp_decks/players

    #game_win_probability_sym_given_match_not_tie
    #game_win_probability_unsym_match_not_tie

    prob_went_2_1_sym= 2*game_win_probability_sym_given_match_not_tie**2
    prob_went_2_1_unsym= 2*game_win_probability_unsym_given_match_not_tie*(1-game_win_probability_unsym_given_match_not_tie)
    distribution_gw={}
    for i in ways_to_get_score:
        #comp
        wins=2*i[0]+i[1]
        games=2*(i[1]+i[0]+i[2])

        comp_distribution_to_add={(wins,games):i[3]*num_comp_this_level}
        for j in range(i[0]):
            new_prob={}
            new_prob[(0,1)]=prob_went_2_1_sym*prop_comp+ prob_went_2_1_unsym*prop_uncomp
            new_prob[(0,0)]=(1-prob_went_2_1_sym)*prop_comp+ (1-prob_went_2_1_unsym)*prop_uncomp
            comp_distribution_to_add= add_probability_distributions(comp_distribution_to_add, new_prob)
        for k in range(i[2]):
            new_prob={}
            new_prob[(1,1)]=prob_went_2_1_sym*prop_comp+ prob_went_2_1_unsym*prop_uncomp
            new_prob[(0,0)]=(1-prob_went_2_1_sym)*prop_comp+ (1-prob_went_2_1_unsym)*prop_uncomp
            comp_distribution_to_add= add_probability_distributions(comp_distribution_to_add, new_prob)
        

        #uncomp
        uncomp_distribution_to_add={(wins,games):i[3]*num_uncomp_this_level}
        for j in range(i[0]):
            new_prob={}
            new_prob[(0,1)]=prob_went_2_1_sym*prop_uncomp+ prob_went_2_1_unsym*prop_comp
            new_prob[(0,0)]=(1-prob_went_2_1_sym)*prop_uncomp+ (1-prob_went_2_1_unsym)*prop_comp
            uncomp_distribution_to_add= add_probability_distributions(uncomp_distribution_to_add, new_prob)
        for k in range(i[2]):
            new_prob={}
            new_prob[(1,1)]=prob_went_2_1_sym*prop_uncomp+ prob_went_2_1_unsym*prop_comp
            new_prob[(0,0)]=(1-prob_went_2_1_sym)*prop_uncomp+ (1-prob_went_2_1_unsym)*prop_comp
            uncomp_distribution_to_add= add_probability_distributions(uncomp_distribution_to_add, new_prob)

        new_dist_to_combine=combine_distributions(comp_distribution_to_add, uncomp_distribution_to_add)
        #now add to the main distribution
        distribution_gw=combine_distributions(distribution_gw, new_dist_to_combine)






    cut_off=(players-winning_group-players_beat)
    scores_of_others_unfixed=list(distribution_gw.keys())
    distribution_to_consider={}
    for i in scores_of_others_unfixed:
        if i[0]/ i[1] in distribution_to_consider:
            distribution_to_consider[i[0]/i[1]]+=distribution_gw[i]
        else:
            distribution_to_consider[i[0]/i[1]]=distribution_gw[i]

    scores_of_others=list(distribution_to_consider.keys())

    scores_of_others.sort()
    running_sum=0
    for i in range(len(scores_of_others)):
        if running_sum<=cut_off and running_sum+distribution_to_consider[scores_of_others[i]]>cut_off:
            out1=scores_of_others[i]
            if i+1 < len(scores_of_others):
                out2=scores_of_others[i+1]
                running_sum_2=running_sum+distribution_to_consider[scores_of_others[i+1]]
            else:
                out2=False
                running_sum_2=0
            cut_off-=running_sum
            break
        running_sum+=distribution_to_consider[scores_of_others[i]]
    return (out1,running_sum,out2,running_sum_2,distribution_gw)

def naive_distribution_of_gw(probability_of_winning_losing,probability_of_going_2_1,matches):
    naive_distribution_of_scores(probability_of_winning_losing,matches)
    prob_distribution_of_opponent_gw_without_you={}
    oppo_possibilities=full_dictionary_of_all_scores_as_dict_of_dict[matches]
    oppo_scores=list(oppo_possibilities.keys())
    oppo_scores.sort()
    for i in oppo_scores: 
        for j in oppo_possibilities[i]:
            wins=2*j[0]
            games=2*(j[0]+j[1]+j[2])
            uncomp_distribution_to_add={(wins,games):i[3]*j[3]*probability_of_winning_losing**(j[0]+j[2])*(1-probability_of_winning_losing)**(j[1])}
            for k in range(j[0]): 
                new_prob={}
                new_prob[(0,1)]=probability_of_going_2_1
                new_prob[(0,0)]=1-probability_of_going_2_1
                uncomp_distribution_to_add= add_probability_distributions(uncomp_distribution_to_add, new_prob)
            for k in range(j[2]):
                new_prob={}
                new_prob[(1,1)]=probability_of_going_2_1
                new_prob[(0,0)]=1-probability_of_going_2_1
                uncomp_distribution_to_add= add_probability_distributions(uncomp_distribution_to_add, new_prob)
        prob_distribution_of_opponent_gw_without_you=combine_distributions(prob_distribution_of_opponent_gw_without_you,uncomp_distribution_to_add)
    return prob_distribution_of_opponent_gw_without_you


def opponent_game_win_prop(score,score_cutoff_data,players_beat,opponent_gw_from_you):

    ways_to_get_score=full_dictionary_of_all_scores[(matches,score)]
    proportion_of_comp_decks=(players-number_of_uncomp_decks)/players
    proportion_of_uncomp_decks=number_of_uncomp_decks/players
    prob_went_2_1_sym= 2*game_win_probability_sym_given_match_not_tie**2
    prob_went_2_1_unsym= 2*game_win_probability_unsym_given_match_not_tie*(1-game_win_probability_unsym_given_match_not_tie)
    
    general_prob_of_2_1= (proportion_of_comp_decks^2+proportion_of_uncomp_decks**2)*prob_went_2_1_sym+2*proportion_of_comp_decks*proportion_of_uncomp_decks*prob_went_2_1_unsym
    
    general_prob_of_winning_or_losing= (1/2)*proportion_of_comp_decks^2*(1-probability_of_match_ties_between_comp_decks)+proportion_of_uncomp_decks^2*(1-probability_of_match_ties_between_comp_decks)+2*proportion_of_comp_decks*proportion_of_uncomp_decks*(1-probability_of_match_ties_between_mismatched_decks)

    
    
    distribution_opponent_gw_without_you=naive_distribution_of_gw(general_prob_of_winning_or_losing,general_prob_of_2_1,matches-1)

    distribution_to_consider_unfixed=distribution_opponent_gw_without_you.copy()
    for i in range(matches-2):
        distribution_to_consider_unfixed=add_probability_distributions(distribution_to_consider_unfixed,distribution_opponent_gw_without_you)
    distribution_to_consider_unfixed=add_probability_distributions(distribution_to_consider_unfixed,opponent_gw_from_you)


    scores_of_others_unfixed=list(distribution_to_consider_unfixed.keys())
    distribution_to_consider={}
    for i in scores_of_others_unfixed:
        if i[0]/ i[1] in distribution_to_consider:
            distribution_to_consider[i[0]/i[1]]+=distribution_to_consider_unfixed[i]
        else:
            distribution_to_consider[i[0]/i[1]]=distribution_to_consider_unfixed[i]


    cut_off=(players-winning_group-players_beat)
    scores_of_others=list(distribution_to_consider.keys())
    scores_of_others.sort()
    running_sum=0
    for i in range(len(scores_of_others)):
        if running_sum<=cut_off and running_sum+distribution_to_consider[scores_of_others[i]]>cut_off:
            out1=scores_of_others[i]
            if i+1 < len(scores_of_others):
                out2=scores_of_others[i+1]
                running_sum_2=running_sum+distribution_to_consider[scores_of_others[i+1]]
            else:
                out2=False
                running_sum_2=0
            cut_off-=running_sum
            break
        running_sum+=distribution_to_consider[scores_of_others[i]]
    return (out1,running_sum,out2,running_sum_2)


def find_tie_breakers(score, score_cutoff_data, players_beat):
    out=[0,0,0,0]
    out[0]=score


    omw_results=opponent_match_win_prop(score, players_beat)

    out[1]=omw_results[0]
    players_beat+=omw_results[1]
    
    gw_results=game_win_prop(score,score_cutoff_data,players_beat)
    
    out[2]=gw_results[0]
    players_beat+=gw_results[1]

    opponents_game_win_from_you={}    

    for i in gw_results[4].keys():
        opponents_game_win_from_you[(i[1]-i[0],i[1])]=gw_results[4][i]




    ogw_results=opponent_game_win_prop(score,score_cutoff_data,players_beat,opponents_game_win_from_you)

    out[3]=ogw_results[2]
    players_beat+=ogw_results[3]

    if out[3] == False:
        out[2]=gw_results[2]
        out[3]=0
        if out[2]== False:
            out[1]=omw_results[2]
            out[2]=0
            if out[1]== False:
                scores=list(full_dictionary_of_all_scores_as_dict_of_dict.keys())
                scores.sort()
                next_score=0
                for i in range(len(scores)):
                    if scores[i] < score:
                        continue
                    if scores[i] > score:
                        next_score=scores[i]
                        break
                out[0]=next_score
                out[1]=0
    return out

def outcome_to_top_8(dict_of_points_and_proportions):
    #output is a tuple
    #tuple has (points value, OMW, GW, and OGW) which you need to have to have a nearly guaranteed top 8
    summed_proportions=find_proportions(dict_of_points_and_proportions)
    scores= list(summed_proportions.keys())
    scores.sort()
    out=[0,0,0,0]
    proportion_of_winners=players/winning_group
    for i in range(len(scores)-1):
        if summed_proportions[scores[i]]<=players-winning_group and summed_proportions[scores[i+1]]>players-winning_group:
            out[0]=scores[i]
            cutoff_score=i
            break
    score_cutoff_data=dict_of_points_and_proportions[out[0]]
    score_cutoff_data_people_beat=summed_proportions[out[0]]

    out=find_tie_breakers(out[0],score_cutoff_data, score_cutoff_data_people_beat)
    return out

def function_outputting_value_of_interest():

    
    if last_match_is_normal:
        score_distribution=Proportion_of_comp_v_noncomp_decks_with_certain_score()
    else:
        almost_full_score_distribution=Proportion_of_comp_v_noncomp_decks_with_certain_score(matches-1)
        score_distribution=round_with_drawers(almost_full_score_distribution)
    return outcome_to_top_8(score_distribution)