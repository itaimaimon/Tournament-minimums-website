
class ScoreData:
    """
    A data class to represent structured report output.
    """
    def __init__(self, points: int, OMW: float, GW: float, OGW: float):
        self.points=points
        self.OMW=OMW
        self.GW=GW
        self.OGW=OGW
        
