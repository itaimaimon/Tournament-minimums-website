from score_class import ScoreData
from input_class import InputData
import random


class PlayerData:
    """
    A data class to represent structured report output.
    """
    def __init__(self,key: int,Comp:bool, MatchesWon: int, MatchesLost: int,MatchesTied: int,OpponentsPlayed: list[int],GamesWon: int,GamesLost: int,GamesTied: int):
        self.key=key
        self.Comp= Comp
        self.MatchesWon= MatchesWon
        self.MatchesLost=MatchesLost
        self.MatchesTied=MatchesTied
        self.OpponentsPlayed=OpponentsPlayed
        self.GamesWon=GamesWon
        self.GamesLost=GamesLost
        self.GamesTied=GamesTied
        self.Score: ScoreData | None = None 
    
    def get_points(self, data: InputData):
        return self.MatchesWon*data.pointsPerWin+self.MatchesLost*data.pointsPerLoss+self.MatchesTied*data.pointsPerTie

class AllPlayerData:
    def __init__(self, GameData:InputData):
        self.GameData=GameData
        self.DictPlayers= {}
        self.DictPlayersScores={}
        self.Uncomp= random.sample(range(0,GameData.numPlayers),GameData.numUncomp)

        for i in range(GameData.numPlayers):
            new_player=PlayerData(key=i,Comp=(i in self.Uncomp),MatchesWon=0,MatchesLost=0,MatchesTied=0,OpponentsPlayed=[],GamesWon=0,GamesLost=0,GamesTied=0)
            new_scoredata= ScoreData(points=0,OMW=0,GW=0,OGW=0)
            new_player.Score=new_scoredata
            self.DictPlayers[i]=new_player
            self.DictPlayersScores[i]=new_scoredata

    
    def Set_Scores(self):
        for i in self.DictPlayers.keys():
            player=self.DictPlayers[i]
            points_i= self.GameData.pointsPerWin*player.MatchesWon+self.GameData.pointsPerLoss*player.MatchesLost+self.GameData.pointsPerTie*player.MatchesTied
            GW_total=(player.GamesWon+player.GamesLost+player.GamesTied)
            if GW_total == 0:
                GW_i=0
            else:
                GW_i= player.GamesWon/GW_total
            OMW_total=0
            OM_total=0
            OGW_total=0
            OG_total=0
            for i in player.OpponentsPlayed:
                OMW_total+=self.DictPlayers[i].MatchesWon
                OM_total+=self.DictPlayers[i].MatchesWon+ self.DictPlayers[i].MatchesLost + self.DictPlayers[i].MatchesTied
                OGW_total+=self.DictPlayers[i].GamesWon
                OG_total+=self.DictPlayers[i].GamesWon+ self.DictPlayers[i].GamesLost + self.DictPlayers[i].GamesTied
            if OM_total == 0:
                OMW_i=0
            else:
                OMW_i=OMW_total/OM_total
            if OG_total==0:
                OGW_i=0
            else:
                OGW_i=OGW_total/OG_total
            Score_i = ScoreData(points=points_i,OMW=OMW_i,GW=GW_i,OGW=OGW_i)
            player.Score=Score_i
            self.DictPlayersScores[i]= Score_i