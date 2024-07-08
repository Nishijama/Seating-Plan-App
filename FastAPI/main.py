# packages
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel
import json

# local files
from database import SessionLocal, engine
import models

app = FastAPI()

# allow origin from the React app
origins = ['http://localhost:3000']
app.add_middleware(CORSMiddleware, allow_origins=origins)


class Attendee(BaseModel):
    first_name: str
    last_name: str
    family: str
    tier: int 
    so: int | None
    table: int = 0


class UpdateAttendee(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    family: str | None = None
    tier: int | None = None
    so: int | None = None
    table: int | None = None

class AttendeeModel(Attendee):
    id: int

    class Config:
        orm_mode = True

# SET UP DATABASE CONNECTION
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# DEPENDENCY INJECTION - TO UNDERSTAND
db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/attendees/{id}", response_model=AttendeeModel)
async def read_attendees(id: int, db: db_dependency, skip: int = 0, limit: int = 100):
    attendee = db.query(models.Attendee).filter(models.Attendee.id == id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Can't edit the attendee. No attendee with provided ID.")
    return attendee


@app.put("/attendees/{id}/", response_model=UpdateAttendee)
async def update_attendee(id: int, attendee_update: UpdateAttendee, db: db_dependency):
    db_attendee = db.query(models.Attendee).filter(models.Attendee.id == id).first()
    
    if not db_attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    
    update_data = attendee_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_attendee, key, value)
    
    db.commit()
    db.refresh(db_attendee)
    
    return db_attendee

@app.get("/attendees/", response_model=list[AttendeeModel])
async def read_attendees(db: db_dependency, skip: int = 0, limit: int = 100):
    attendees = db.query(models.Attendee).offset(skip).limit(limit).all()
    return attendees

@app.post("/attendees/", response_model=AttendeeModel)
async def create_attendees(attendee: AttendeeModel, db: db_dependency):
    db_attendee = models.Attendee(**attendee.model_dump())
    db.add(db_attendee)
    db.commit()
    db.refresh(db_attendee)
    return db_attendee


# @app.delete("/delete_attendee/{id}")
# def delete_attendee(id):
#     if id not in attendees.keys():
#         return {"Error": "Can't delete the attendee. No attendee with provided ID."}
#     attendees.pop(id)
#     return attendees
