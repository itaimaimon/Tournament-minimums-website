from fastapi import FastAPI
from pydantic import BaseModel, conint, Field
from typing import List, Optional, Annotated
from theory import InputData, calculate_minimum_results

# --- FastAPI app ---
app = FastAPI()

# --- Pydantic model to parse frontend JSON ---
class FormData(BaseModel):
    #most input error handling
    numPlayers: Annotated[int,Field(gt=0,default=16)]               
    numMatches: Optional[Annotated[int,Field(gt=0)]] = None
    targetTop: Annotated[int,Field(gt=0, default = 8)]
    gamesPerMatch: Annotated[int,Field(gt=0, default = 3)]
    pointsWin: Annotated[int,Field(default = 3)]
    pointsLoss: Annotated[int,Field(default = 0)]
    pointsTie: Annotated[int,Field(default = 1)]
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
        numMatches=data_dict.get("numMatches"),
        gamesPerMatch=data_dict["gamesPerMatch"],
        pointsWin=data_dict.get("pointsWin"),
        pointsLoss=data_dict.get("pointsLoss"),
        pointsTie=data_dict.get("pointsTie"),
        tiebreakers=data_dict["tiebreakers"],
        allowLastRoundDraw=data_dict["allowLastRoundDraw"],
    )
    
    # Call your calculation function
    result = calculate_minimum_results(input_obj)
    
    # Return JSON response
    return {"result": result}
