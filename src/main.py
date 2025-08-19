from fastapi import FastAPI, HTTPException
from src.dal import Dal

app = FastAPI()
dal = Dal()

@app.get("/soldiersdb")
def get_all_soldiers():
    result = dal.find_all()
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail="Database error")
    return result

@app.post("/soldiersdb")
def create_soldier(soldier: dict):
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
def update_soldier(soldier_id, field, value):
    result = dal.update_soldier(soldier_id,field, value)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "soldier_not_found":
            raise HTTPException(status_code=404, detail="Soldier not found")
        else:
            raise HTTPException(status_code=500, detail="Database error")

    return result

@app.delete("/soldiersdb/{soldier_id}")
def delete_soldier(soldier_id):
    result = dal.delete_soldier(soldier_id)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "soldier_not_found":
            raise HTTPException(status_code=404, detail="Soldier not found")
        else:
            raise HTTPException(status_code=500, detail="Database error")

    return result