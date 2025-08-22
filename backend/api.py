from fastapi import FastAPI
from pydantic import BaseModel, conint, Field
from typing import List, Optional, Annotated
from theory import calculate_minimum_results
from components.input_class import InputData


# --- FastAPI app ---
app = FastAPI()

# --- Pydantic model to parse frontend JSON ---
class FormData(BaseModel):
    #most input error handling
    numPlayers: Annotated[int,Field(gt=0,default=16)]               
    numMatches: Optional[Annotated[int,Field(gt=0)]] = None
    targetTop: Annotated[int,Field(gt=0, default = 8)]
    gamesPerMatch: Annotated[int,Field(gt=0, default = 3)]
    pointsPerWin: Annotated[int,Field(default = 3)]
    pointsPerLoss: Annotated[int,Field(default = 0)]
    pointsPerTie: Annotated[int,Field(default = 1)]
    tiebreakers: List[bool]
    lastMatchIsDraw: bool
    numUncomp: Annotated[int,Field(ge=0, default = 0)]
    probMatchTiesBetweenComp: Annotated[float,Field(ge=0, le=1, default = .1)]
    probMatchTiesBetweenUncomp: Annotated[float,Field(ge=0, le=1, default = .1)]
    probMatchTiesBetweenMismatched: Annotated[float,Field(ge=0, le=1, default = .1)]
    probGameWinBetweenMismatched: Annotated[float,Field(ge=0, le=1, default = .6)]
    probMatchWinBetweenMismatched: Optional[Annotated[float,Field(ge=0, le=1)]]= None
    monteCarloChosen: bool


# --- API route ---
@app.post("/calculate")
def calculate_route(data: FormData):
    # Convert Pydantic model to dict
    data_dict = data.dict()
    
    # Initialize InputData with defaults handled inside class
    input_obj = InputData(

        numPlayers=data_dict["numPlayers"],
        numMatches = data_dict.get("numMatches"),
        gamesPerMatch =data_dict["gamesPerMatch"],
        targetTop = data_dict["targetTop"],
        pointsPerWin =data_dict["pointsPerWin"],
        pointsPerTie =data_dict["pointsPerTie"],
        pointsPerLoss =data_dict["pointsPerLoss"],
        tiebreakers =data_dict["tiebreakers"],
        lastMatchIsDraw =data_dict["lastMatchIsDraw"],
        numUncomp =data_dict["numUncomp"],
        probMatchTiesBetweenComp =data_dict["probMatchTiesBetweenComp"],
        probMatchTiesBetweenUncomp =data_dict["probMatchTiesBetweenUncomp"],
        probMatchTiesBetweenMismatched =data_dict["probMatchTiesBetweenMismatched"],
        probGameWinBetweenMismatched =data_dict["probGameWinBetweenMismatched"],
        probMatchWinBetweenMismatched = data_dict.get("probMatchWinBetweenMismatched"),
        monteCarloChosen =  data_dict["monteCarloChosen"],
    )
    
    # Call your calculation function
    result = calculate_minimum_results(input_obj)
    
    # Return JSON response
    return {"result": result}
