import csv
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File
from classes.soldier import Soldier
from classes.base import Base
from classes.dwellings import Dwellings


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome to Housing Management System!"}


@app.post("/assignWithCsv")
async def assignWithCsv(csvFile: UploadFile = File(...)):
    seven_sheaves = Base()
    seven_sheaves.add_dwelling(Dwellings(1))
    seven_sheaves.add_dwelling(Dwellings(2))

    content = await csvFile.read()
    lines = content.decode().splitlines()
    reader = csv.DictReader(lines)
    for row in reader:
        if valid_input(row):
            seven_sheaves.add_soldier(Soldier(row["מספר אישי"], row["שם פרטי"], row["שם משפחה"], row["מין"], row["עיר מגורים"], int(row["מרחק מהבסיס"])))
    seven_sheaves.assignment_by_distance()
    return {
            "number of assigned soldiers" : len(seven_sheaves.list_of_assigned_soldiers),
            "number of unassigned soldiers" : len(seven_sheaves.list_of_unassigned_soldiers),
            "assigned soldiers" : [s.__dict__ for s in seven_sheaves.list_of_assigned_soldiers],
            "unassigned soldiers" : [s.__dict__ for s in seven_sheaves.list_of_unassigned_soldiers]
            }

def valid_input(row):
    if row["מספר אישי"][0] != "8" or not row["מספר אישי"].isdigit():
        return False
    if not row["מרחק מהבסיס"].isdigit():
        return False
    return True



if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=8000)

