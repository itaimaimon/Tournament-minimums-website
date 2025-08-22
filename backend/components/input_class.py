import math

class InputData:
    def __init__(self,numPlayers,numMatches, gamesPerMatch, targetTop, pointsPerWin, pointsPerTie, pointsPerLoss, tiebreakers, lastMatchIsDraw, 
        numUncomp,probMatchTiesBetweenComp, probMatchTiesBetweenUncomp,probMatchTiesBetweenMismatched,probGameWinBetweenMismatched, 
        probMatchWinBetweenMismatched,monteCarloChosen):
        
        self.monteCarloChosen=monteCarloChosen
            #default: false
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
        self.probMatchTiesBetweenComp=probMatchTiesBetweenComp
            #default: .1
        self.probMatchTiesBetweenUncomp= probMatchTiesBetweenUncomp
            #default: .1
        self.probGameWinBetweenMatchedDecks=.5
            #maybe take away as is not variable?
        self.probGameWinBetweenMismatched=probGameWinBetweenMismatched
            #default: .6 
        self.probMatchWinBetweenCompDecks = .5-probMatchTiesBetweenComp/2
            # maybe take away as is not variable?
        self.proMatchWinBetweenUncompDecks = .5-probMatchTiesBetweenUncomp/2
            # maybe take away as is not variable?

        #error handling
        if(probMatchWinBetweenMismatched and probMatchWinBetweenMismatched+probMatchTiesBetweenMismatched>1):
            raise ValueError(f"probability of matches wins + ties cannot be greater than 1")


        (self.probMatchWinBetweenMismatched,self.probMatchTiesBetweenMismatched,self.probMatchLossBetweenMismatched)= \
        match_win_from_game_win_and_ties(probGameWinBetweenMismatched, probMatchTiesBetweenMismatched,gamesPerMatch) if not probMatchWinBetweenMismatched else \
        (probMatchWinBetweenMismatched,probMatchTiesBetweenMismatched,1-probMatchWinBetweenMismatched-probMatchTiesBetweenMismatched)
        # default: (changes probability of match ties in scenarios where this does not make sense (only even games per match scenarios))
        # (probability_of_match_win_between_mismatched_decks,probability_of_match_ties_between_mismatched_decks,probability_of_match_losses_between_mismatched_decks)=match_win_from_game_win_and_ties(probability_of_game_win_between_mismatched_decks, probability_of_match_ties_between_mismatched_decks,games_per_match)
          

        #last bit of error handling 
        if(self.probMatchWinBetweenMismatched+self.probMatchTiesBetweenMismatched+self.probMatchLossBetweenMismatched>1):
            raise ValueError(f"probability of matches loss + wins + ties cannot be greater than 1")
        if(self.probMatchWinBetweenMismatched<0 or self.probMatchWinBetweenMismatched>1):
            raise ValueError(f"probability of matches wins cannot be greater than 1 or less than 0")
        if(self.probMatchTiesBetweenMismatched<0 or self.probMatchTiesBetweenMismatched>1):
            raise ValueError(f"probability of matches loss cannot be greater than 1 or less than 0")
        if(self.probMatchLossBetweenMismatched<0 or self.probMatchLossBetweenMismatched>1):
            raise ValueError(f"probability of matches ties cannot be greater than 1 or less than 0")

def event_probs(i,j,p_i,p_j):
    return math.comb(i+j,i)*p_i**i*p_j**j

def match_win_from_game_win_and_ties(game_win_probability, match_tie_probability,Num_games):
    """
    Calculate the probability of winning a match given the probabilities of winning a game and tying a match.
    we decide this based on the fact that for odd games per match, a match tie occurs almost only when time is reached on the last game in a match. 
    as (true) game ties are incredibly low probability events. thus we decide that the proportion of match wins vs match losses 
    can be estimated with all the necessary assumptions and match ties accounted to at the end.
    """
    game_loss_probability=1-game_win_probability

    match_win_prob=0

    for i in range(math.ceil(Num_games/2)):
        match_win_prob+=event_probs(math.floor(Num_games/2)+1,i,game_win_probability,game_loss_probability)

    if(Num_games%2==1):
        return (match_win_prob*(1-match_tie_probability),match_tie_probability,(1-match_win_prob)*(1-match_tie_probability))
    else:
        """If games per match are even we also caclulate match_tie_probability and if it is lower adjust while keeping proportions of wins and losses the same
          and if it is higher then we just return these values and assume that the tie probability is higher than the user expected"""
        calculated_match_tie_probability= event_probs(Num_games/2,Num_games/2,game_win_probability,game_loss_probability)
        if(calculated_match_tie_probability-match_tie_probability>0):
            return (match_win_prob,calculated_match_tie_probability,1-match_win_prob-match_tie_probability)
        else:
            offset=(1-match_tie_probability)/(1-calculated_match_tie_probability)
            return (match_win_prob*offset,match_tie_probability,1-match_win_prob*(offset)-match_tie_probability)