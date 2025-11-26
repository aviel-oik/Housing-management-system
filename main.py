import csv
import uvicorn
import sqlite3
from fastapi import FastAPI, HTTPException, UploadFile, File
from classes.soldier import Soldier
from classes.base import Base


app = FastAPI()

seven_sheaves = Base("seven_sheaves", 2)

@app.get("/")
def read_root():
    return {"message": "Welcome to Housing Management System!"}


@app.post("/assignWithCsv")
async def assignWithCsv(csvFile: UploadFile = File(...)):
    reset_data()
    content = await csvFile.read()
    lines = content.decode().splitlines()
    reader = csv.DictReader(lines)
    for row in reader:
        if valid_input(row):
            seven_sheaves.add_soldier(Soldier(row["מספר אישי"], row["שם פרטי"], row["שם משפחה"], row["מין"], row["עיר מגורים"], int(row["מרחק מהבסיס"])))
    seven_sheaves.assign()
    return {
            "number of assigned soldiers" : len(seven_sheaves.list_of_assigned_soldiers),
            "number of unassigned soldiers" : len(seven_sheaves.list_of_unassigned_soldiers),
            "assigned soldiers" : [s.__dict__ for s in seven_sheaves.list_of_assigned_soldiers],
            "unassigned soldiers" : [s.__dict__ for s in seven_sheaves.list_of_unassigned_soldiers]
            }

def reset_data():
    for dwelling in seven_sheaves.list_of_dwellings:
        dwelling.empty_rooms()
    seven_sheaves.list_of_assigned_soldiers = []
    seven_sheaves.list_of_unassigned_soldiers = []

def valid_input(row):
    if row["מספר אישי"][0] != "8" or not row["מספר אישי"].isdigit():
        return False
    if not row["מרחק מהבסיס"].isdigit():
        return False
    return True


@app.get("/space")
def space():
    num_of_empty = 0
    num_of_part = 0
    num_of_full = 0
    for dwelling in seven_sheaves.list_of_dwellings:
        for room in dwelling.list_of_rooms:
            if room.space == "full":
                num_of_full += 1
            elif room.space == "empty":
                num_of_empty += 1
            else:
                num_of_part += 1
    return {
            "number of empty rooms" : num_of_empty,
            "number of part rooms" : num_of_part,
            "number of full rooms" : num_of_full
            }


@app.get("/waitingList")
def waitingList():
    return {
            "unassigned soldiers" : [s.__dict__ for s in seven_sheaves.list_of_unassigned_soldiers]
            }


@app.get("/search/{id}")
def search(id):
    soldier = None
    for s in seven_sheaves.list_of_unassigned_soldiers:
        if int(s.id) == int(id):
            soldier = s
    if soldier:
        return {
                "assigned" : soldier.assignment_status,
                "status" : "Waiting"
                }
    else:
        for s in seven_sheaves.list_of_assigned_soldiers:
            if int(s.id) == int(id):
                soldier = s
        if soldier:
            return {
                    "assigned" : soldier.assignment_status,
                    "Dwellings number" : soldier.dwellings_assigned,
                    "room number" : soldier.room_assigned
                    }
    return {"message" : "No such soldier found"}


@app.post("/initializeScheme")
def initializeScheme():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Unassigned_Soldiers(
        id TEXT PRIMARY KEY,
        first_name TEXT
        last_name TEXT,
        gender TEXT,
        city_of_residence TEXT,
        distance_from_base INTEGER,
        assignment_status TEXT,
        dwellings_assigned TEXT,
        room_assigned TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Assigned_Soldiers(
        id TEXT PRIMARY KEY,
        first_name TEXT
        last_name TEXT,
        gender TEXT,
        city_of_residence TEXT,
        distance_from_base INTEGER,
        assignment_status TEXT,
        dwellings_assigned TEXT,
        room_assigned TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Base(
        name TEXT PRIMARY KEY
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Dwellings(
        building_number TEXT PRIMARY KEY,
        base_name TEXT 
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Room(
        room_num TEXT PRIMARY KEY,
        space TEXT 
    );
    """)
    conn.commit()
    conn.close()
    return {"message": "initialization confirmed"}



if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=8000)

