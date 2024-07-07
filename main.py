from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
import json

app = FastAPI()

class Attendee(BaseModel):
    first_name: str
    last_name: str
    family: str
    tier: int 
    #tiers: 0 - special, 1 - close family, 2 - family & friends
    so: int | None
    table: int = 0

class UpdateAttendee(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    family: Optional[str] = None
    tier: Optional[int] = None
    so: Optional[int] = None
    table: Optional[int] = None


def read_json_file(file):
    f = open(file)
    data = json.load(f)
    int_key_data = {int(k): v for k, v in data.items()}
    return int_key_data

def save_json_file(data):
    f = open('data.json', 'w')
    json.dump(data, f)
    return

attendees = read_json_file('data.json')

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/attendee/{id}")
def read_attendee(id: int):
    if id not in attendees.keys():
        return {"Error": "Can't edit the attendee. No attendee with provided ID."}
    return attendees[id]



@app.put("/attendee/{id}")
def update_attendee(id: int, attendee: UpdateAttendee):

    if id not in attendees.keys():
        return {"Error": "Can't edit the attendee. No attendee with provided ID."}

    for k,v in vars(attendee).items():
        if not v is None:
            attendees[id][k] = v
    save_json_file(attendees)
    return attendees[id]


@app.post("/attendee/{id}")
def create_attendee(attendee: Attendee):
    if not attendee[id]:
        new_id = len(attendees)
        attendees[new_id] = attendee
        save_json_file(attendees)
        return attendees[new_id]

@app.get("/attendees/")
def read_attendees():
    return attendees

@app.delete("/delete_attendee/{id}")
def delete_attendee(id):
    if id not in attendees.keys():
        return {"Error": "Can't delete the attendee. No attendee with provided ID."}
    attendees.pop(id)
    return attendees
