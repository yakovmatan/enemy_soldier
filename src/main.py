from fastapi import FastAPI, HTTPException
from dal import Dal
from pydantic import BaseModel

app = FastAPI()
dal = Dal()


class SoldierData(BaseModel):
    soldierID: int
    firstName: str
    lastName: str
    phoneNumber:str
    rank: str

@app.get("/soldiersdb")
def get_all_soldiers():
    result = dal.find_all()
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail="Database error")
    return result

@app.post("/soldiersdb")
def create_soldier(soldier: SoldierData):
    result = dal.insert_soldier(soldier)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "soldier_exists":
            raise HTTPException(status_code=409, detail="Soldier already exists")
        elif result["error"] == "validation_failed":
            raise HTTPException(status_code=400, detail="Invalid soldier data")
        else:
            raise HTTPException(status_code=500, detail="Database error")

    return result

@app.put("/soldiersdb/{soldier_id}/{field}/{value}")
def update_soldier(soldier_id: int, field: str, value: str):
    result = dal.update_soldier(soldier_id,field, value)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "soldier_not_found":
            raise HTTPException(status_code=404, detail="Soldier not found")
        else:
            raise HTTPException(status_code=500, detail="Database error")

    return result

@app.delete("/soldiersdb/{soldier_id}")
def delete_soldier(soldier_id: int):
    result = dal.delete_soldier(soldier_id)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "soldier_not_found":
            raise HTTPException(status_code=404, detail="Soldier not found")
        else:
            raise HTTPException(status_code=500, detail="Database error")

    return result