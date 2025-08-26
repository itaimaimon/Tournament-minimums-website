from fastapi import FastAPI
from pydantic import BaseModel, conint, Field, AfterValidator, ValidationError
from typing import List, Optional, Annotated
from backend.theory import calculate_minimum_results
from backend.components.input_class import InputData
from annotated_types import Len

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
    probLastGameTiesBetweenComp: Annotated[float,Field(ge=0, le=1, default = .1)]
    probLastGameTiesBetweenUncomp: Annotated[float,Field(ge=0, le=1, default = .1)]
    probLastGameTiesBetweenMismatched: Annotated[float,Field(ge=0, le=1, default = .1)]
    probGameWinBetweenMismatched: Annotated[float,Field(ge=0, le=1, default = .6)]
    monteCarloChosen: bool
    monteCarloIterations: Annotated[int,Field(gt=0, le=2000,default=10)]


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
        probLastGameTiesBetweenComp =data_dict["probLastGameTiesBetweenComp"],
        probLastGameTiesBetweenUncomp =data_dict["probLastGameTiesBetweenUncomp"],
        probLastGameTiesBetweenMismatched =data_dict["probLastGameTiesBetweenMismatched"],
        probGameWinBetweenMismatched =data_dict["probGameWinBetweenMismatched"],
        monteCarloChosen =  data_dict["monteCarloChosen"],
        monteCarloIterations = data_dict.get("monteCarloIterations"),
    )
    
    # Call your calculation function
    result = calculate_minimum_results(input_obj)
    
    # Return JSON response
    return {"result": result}
