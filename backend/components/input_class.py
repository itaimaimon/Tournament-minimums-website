import math

class InputData:
    def __init__(self,numPlayers,numMatches, gamesPerMatch, targetTop, pointsPerWin, pointsPerTie, pointsPerLoss, tiebreakers, lastMatchIsDraw, 
        numUncomp,probLastGameTiesBetweenComp, probLastGameTiesBetweenUncomp,probLastGameTiesBetweenMismatched,probGameWinBetweenMismatched,minDrawProb,monteCarloIterations):
        
        self.monteCarloChosen=True
            #always true change if want direct calc to be implemented

        self.monteCarloIterations= monteCarloIterations if monteCarloIterations%2==1 else monteCarloIterations+1

        self.minDrawProb=minDrawProb
            #default: .9

        self.numPlayers = numPlayers
            #default: 16
        self.numMatches = math.ceil(math.log(numPlayers,2)) if not numMatches else numMatches 
            #default: matches=math.ceil(math.log(players,2))
        self.gamesPerMatch= gamesPerMatch
            #default: 3
        self.pointsPerWin = pointsPerWin
            #default: 3
        self.pointsPerTie = pointsPerTie
            #default: 1
        self.pointsPerLoss= pointsPerLoss
            #default: 0
        self.tiebreakers= tiebreakers
            #default: ['omw','gw','ogw']
        self.targetTop = targetTop
            #default: 8
        self.lastMatchIsDraw=lastMatchIsDraw
            #default: True

        #error handling 
        if(numUncomp>numPlayers):
            raise ValueError(f"numUncomp must be a less than or equal to numPlayers")
        
        self.numUncomp = numUncomp
            #default: 0
        self.probLastGameTiesBetweenComp=probLastGameTiesBetweenComp
            #default: .1
        self.probLastGameTiesBetweenUncomp= probLastGameTiesBetweenUncomp
            #default: .1
        self.probLastGameTiesBetweenMismatched= probLastGameTiesBetweenMismatched
            #default: .05

        self.probGameWinBetweenMatchedDecks=.5
            #maybe take away as is not variable?
        self.probGameWinBetweenMismatched=probGameWinBetweenMismatched
            #default: .6 


        #take in random variable betweeon 0-1 output (player_one_outcomes,player_two_outcomes) 
        #always assumes player one is advantaged if mismatched
        #outcomes of form ('won'/'lost'/'tied',games_won, games_lost,games_tied,total_games)
        
        (self.funcMatchOutcomesComp,self.listCutoffsComp)= match_outcome_function(self.probGameWinBetweenMatchedDecks,self.gamesPerMatch,self.probLastGameTiesBetweenComp)
        (self.funcMatchOutcomesUncomp,self.listCutoffsUncomp)= match_outcome_function(self.probGameWinBetweenMatchedDecks,self.gamesPerMatch,self.probLastGameTiesBetweenUncomp)
        (self.funcMatchOutcomesMismatched,self.listCutoffsMismatched)= match_outcome_function(self.probGameWinBetweenMismatched,self.gamesPerMatch,self.probLastGameTiesBetweenMismatched)

        if not self.monteCarloChosen:
            self.probability_of_match_ties_between_comp_decks=self.listCutoffsComp[1]
            self.probability_of_match_ties_between_uncomp_decks=self.listCutoffsUncomp[1]
            self.probability_of_match_ties_between_mismatched_decks=self.listCutoffsMismatched[1]

            if(self.gamesPerMatch%2==1):
                if self.gamesPerMatch==1:
                    self.probability_of_match_win_between_mismatched_decks=self.listCutoffsMismatched[2]-self.listCutoffsMismatched[1]
                else:
                    self.probability_of_match_win_between_mismatched_decks=self.listCutoffsMismatched[math.floor(self.gamesPerMatch/2)+3]-self.listCutoffsMismatched[3]+self.listCutoffsMismatched[2]-self.listCutoffsMismatched[1]
            else:
                if self.gamesPerMatch==2:
                    self.probability_of_match_win_between_mismatched_decks=self.listCutoffsMismatched[4]-self.listCutoffsMismatched[3]+self.listCutoffsMismatched[2]-self.listCutoffsMismatched[1]
                else: 
                    self.probability_of_match_win_between_mismatched_decks=self.listCutoffsMismatched[math.floor(self.gamesPerMatch/2)+3]-self.listCutoffsMismatched[5]+self.listCutoffsMismatched[4]+ self.listCutoffsMismatched[3]+self.listCutoffsMismatched[2]-self.listCutoffsMismatched[1]


def event_probs(i,j,p_i,p_j):
    if not i==j:
        if i>j:
            return get_to_step_n(i-1,j,p_i,p_j)*p_i #adjusted so that the winner wins on the last game e.g. doesn't count winning earlier and playing extra games for fun in stats
        else:
            return get_to_step_n(i,j-1,p_i,p_j)*p_j #needed if to deal with when j-1=-1 or i-1 =-1
    else:
        return get_to_step_n(i,j,p_i,p_j) #do not need to adjust for ties

def get_to_step_n(i,j,p_i,p_j):
    return math.comb(int(i+j),int(max(i,j)))*p_i**i*p_j**j

def generate_list_of_cutoffs(game_win_prob_player_one, games_per_match, ProbLastGameTies):
    if( games_per_match%2==1):
        #deal with last game tie problems
        prob_match_tie= event_probs(math.floor(games_per_match/2),math.floor(games_per_match/2),game_win_prob_player_one,1-game_win_prob_player_one)*(ProbLastGameTies)
        prob_match_win_by_one= event_probs(math.ceil(games_per_match/2),math.floor(games_per_match/2),game_win_prob_player_one,1-game_win_prob_player_one)*(1-ProbLastGameTies)
        prob_match_lose_by_one= event_probs(math.floor(games_per_match/2),math.ceil(games_per_match/2),game_win_prob_player_one,1-game_win_prob_player_one)*(1-ProbLastGameTies)
    
        list_of_cutoffs=[0,prob_match_tie,prob_match_win_by_one+prob_match_tie,prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie]
        curr_prob=prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie
        for i in range(math.floor(games_per_match/2)):
            curr_prob+= event_probs(math.ceil(games_per_match/2),i,game_win_prob_player_one,1-game_win_prob_player_one)
            list_of_cutoffs.append(curr_prob)
        for i in range(math.floor(games_per_match/2)):
            curr_prob+= event_probs(i,math.ceil(games_per_match/2),game_win_prob_player_one,1-game_win_prob_player_one)
            list_of_cutoffs.append(curr_prob)
    else:
        prob_match_tie= event_probs(games_per_match/2,games_per_match/2,game_win_prob_player_one,1-game_win_prob_player_one)*(1-ProbLastGameTies)
        prob_match_win_by_two=event_probs(games_per_match/2+1,games_per_match/2-1,game_win_prob_player_one,1-game_win_prob_player_one)*(1-ProbLastGameTies)
        prob_match_lose_by_two=event_probs(games_per_match/2-1,games_per_match/2+1,game_win_prob_player_one,1-game_win_prob_player_one)*(1-ProbLastGameTies)
        
        prob_match_win_by_one=get_to_step_n(games_per_match/2,games_per_match/2-1,game_win_prob_player_one,1-game_win_prob_player_one)*(ProbLastGameTies)
        prob_match_lose_by_one= get_to_step_n(games_per_match/2-1,games_per_match/2,game_win_prob_player_one,1-game_win_prob_player_one)*(ProbLastGameTies)
    
        list_of_cutoffs=[0,prob_match_tie,prob_match_win_by_one+prob_match_tie,prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie,\
                             prob_match_win_by_two +prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie,prob_match_lose_by_two+prob_match_win_by_two +prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie]
        
        curr_prob=prob_match_lose_by_two+prob_match_win_by_two +prob_match_lose_by_one+prob_match_win_by_one+prob_match_tie
        for i in range(math.floor(games_per_match/2)-1):
            curr_prob+= event_probs(games_per_match/2+1,i,game_win_prob_player_one,1-game_win_prob_player_one)
            list_of_cutoffs.append(curr_prob)
        for i in range(math.floor(games_per_match/2)-1):
            curr_prob+= event_probs(i,games_per_match/2+1,game_win_prob_player_one,1-game_win_prob_player_one)
            list_of_cutoffs.append(curr_prob)
    return list_of_cutoffs

def match_outcome_function(game_win_prob_player_one, games_per_match, ProbLastGameTies):

    list_of_cutoffs=generate_list_of_cutoffs(game_win_prob_player_one,games_per_match,ProbLastGameTies)
    #odd case
    if( games_per_match%2==1):
        #define output function
        def output_function(random_number):

            #initialized for error checking
            player_one_match_outcome= 'init'
            player_two_match_outcome= 'init'

            games_tied= 0
            games_won_by_one = 0
            games_won_by_two = 0
            total_games=0


            if(random_number<=list_of_cutoffs[1]):
                #tied done by hand
                player_one_match_outcome= 'tied'
                player_two_match_outcome= 'tied'

                games_tied= 1
                games_won_by_one = math.floor(games_per_match/2)
                games_won_by_two = math.floor(games_per_match/2)
                total_games=games_won_by_one+games_won_by_two+games_tied
  
            elif(random_number<=list_of_cutoffs[2]):
                #win by one done by hand
                player_one_match_outcome= 'won'
                player_two_match_outcome= 'lost'

                games_tied= 0
                games_won_by_one=math.ceil(games_per_match/2)
                games_won_by_two=math.floor(games_per_match/2)
                total_games=games_won_by_one+games_won_by_two+games_tied

            elif(random_number<=list_of_cutoffs[3]):
                #lose by one done by hand
                player_one_match_outcome= 'lost'
                player_two_match_outcome= 'won'

                games_tied= 0
                games_won_by_one=math.floor(games_per_match/2)
                games_won_by_two=math.ceil(games_per_match/2)
                total_games=games_won_by_one+games_won_by_two+games_tied

            else:
                #rest done by loop
                for i in range(3,len(list_of_cutoffs)-1):
                    if (random_number<= list_of_cutoffs[i+1] and random_number>list_of_cutoffs[i]):
                        if i<=games_per_match/2+2: #math.floor(games_per_match/2)+2
                            player_one_match_outcome= 'won'
                            player_two_match_outcome= 'lost'
                            games_won_by_one= math.ceil(games_per_match/2)
                            games_won_by_two=i-3
                            games_tied=0
                            total_games=games_won_by_one+games_won_by_two+games_tied
                        else:
                            player_one_match_outcome= 'lost'
                            player_two_match_outcome= 'won'
                            games_won_by_one= i-math.ceil(games_per_match/2)+2
                            games_won_by_two= math.ceil(games_per_match/2)
                            games_tied=0
                            total_games=games_won_by_one+ games_won_by_two+games_tied
                        break

            player_one_outcome=(player_one_match_outcome, games_won_by_one,games_won_by_two,games_tied, total_games)
            player_two_outcome=(player_two_match_outcome, games_won_by_two,games_won_by_one,games_tied, total_games)
            return (player_one_outcome,player_two_outcome)


    #even case
    else:
        #define output function
        def output_function(random_number):
                        #initialized for error checking
            player_one_match_outcome= 'init'
            player_two_match_outcome= 'init'

            games_tied= 0
            games_won_by_one = 0
            games_won_by_two = 0
            total_games=0




            if(random_number<=list_of_cutoffs[1]):
                #tied done by hand
                players_tied=True
                games_tied= 0
                games_won_by_one = games_per_match/2
                games_won_by_two = games_per_match/2
                total_games=games_won_by_one+games_won_by_two+games_tied

                player_one_match_outcome= 'tied'
                player_two_match_outcome= 'tied'
  
            elif(random_number<=list_of_cutoffs[2]):
                #win by one done by hand
                player_one_match_outcome= 'won'
                player_two_match_outcome= 'lost'

                games_tied= 1
                games_won_by_one=games_per_match/2
                games_won_by_two=games_per_match/2-1
                total_games=games_won_by_one+games_won_by_two+games_tied

            elif(random_number<=list_of_cutoffs[3]):
                #lose by one done by hand
                player_one_match_outcome= 'lost'
                player_two_match_outcome= 'won'

                games_tied= 1
                games_won_by_one=games_per_match/2-1
                games_won_by_two=games_per_match/2
                total_games=games_won_by_one+games_won_by_two+games_tied

            elif(random_number<=list_of_cutoffs[4]):
                #win by 2 done by hand
                player_one_match_outcome= 'won'
                player_two_match_outcome= 'lost'

                games_tied= 0
                games_won_by_one=games_per_match/2+1
                games_won_by_two=games_per_match/2-1
                total_games=games_won_by_one+games_won_by_two+games_tied                
                
            elif(random_number<=list_of_cutoffs[5]):
                #lose by 2 done by hand
                player_one_match_outcome= 'lost'
                player_two_match_outcome= 'won'

                games_tied= 0
                games_won_by_one=games_per_match/2-1
                games_won_by_two=games_per_match/2+1
                total_games=games_won_by_one+games_won_by_two+games_tied    


            else:

                for i in range(5,len(list_of_cutoffs)-1):
                    if (random_number<=list_of_cutoffs[i+1] and random_number>list_of_cutoffs[i]):
                        if i<=games_per_match/2+3: 
                            player_one_match_outcome= 'won'
                            player_two_match_outcome= 'lost'
                            games_won_by_one= games_per_match/2+1
                            games_won_by_two=i-5
                            games_tied=0
                            total_games=games_won_by_one+games_won_by_two+games_tied
                        else:
                            player_one_match_outcome= 'lost'
                            player_two_match_outcome= 'won'
                            games_won_by_one= i-(games_per_match/2+4)
                            games_won_by_two= games_per_match/2+1
                            games_tied=0
                            total_games=games_won_by_one+ games_won_by_two+games_tied
                        break

            player_one_outcome=(player_one_match_outcome, games_won_by_one,games_won_by_two,games_tied, total_games)
            player_two_outcome=(player_two_match_outcome, games_won_by_two,games_won_by_one,games_tied, total_games)
            return (player_one_outcome,player_two_outcome)
    return (output_function,list_of_cutoffs)


"""
made redundant by using function form above

def match_win_from_game_win_and_ties(game_win_probability, prob_last_game_ties,Num_games):
    
    #Calculate the probability of winning a match given the probabilities of winning a game and tying a match.
    #we decide this based on the fact that for odd games per match, a match tie occurs almost only when time is reached on the last game in a match. 
    #as (true) game ties are incredibly low probability events. thus we decide that the proportion of match wins vs match losses 
    #can be estimated with all the necessary assumptions and match ties accounted to at the end.
    
    game_loss_probability=1-game_win_probability

    match_win_prob=0

    for i in range(math.ceil(Num_games/2)):
        match_win_prob+=event_probs(math.floor(Num_games/2)+1,i,game_win_probability,game_loss_probability)

    if(Num_games%2==1):
        return (match_win_prob*(1-prob_last_game_ties),prob_last_game_ties,(1-match_win_prob)*(1-prob_last_game_ties))
    else:
        #If games per match are even we also caclulate match_tie_probability and if it is lower adjust while keeping proportions of wins and losses the same
        #  and if it is higher then we just return these values and assume that the tie probability is higher than the user expected
        calculated_match_tie_probability= (1-prob_last_game_ties)*(event_probs(Num_games/2,Num_games/2,game_win_probability,game_loss_probability))
        return (match_win_prob,calculated_match_tie_probability,1-match_win_prob-calculated_match_tie_probability)

"""