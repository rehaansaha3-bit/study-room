from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime;
from fastapi import HTTPException;
from pydantic import BaseModel, Field, model_validator, field_validator


DB_PATH = "study_room.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


class rooms(Base):
    __tablename__="rooms"

    id = Column(Integer,primary_key = True)
    name = Column(String)
    building = Column(String)
    capacity = Column(Integer)
    has_projector = Column(Integer, default=0)
    is_open = Column(Integer, default=1)


class bookings(Base):
    __tablename__="bookings"

    id = Column(Integer,primary_key = True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    roll_no = Column(Integer)
    booking_date = Column(DateTime, default=datetime.now)
    start_hour = Column(Integer)
    group_size = Column(Integer)
    status = Column(String)
    booked_on = Column(DateTime, default=datetime.now)
    
class Users(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key= True)
    role = Column(String, default = "student")
    user_name = Column(String)
    password= Column(String)


Base.metadata.create_all(engine)

#--------------pydantic----------------

def clean_text(value):
    value = value.strip()
    if value == "":
        raise ValueError("cannot be blank")
    return value

# Used in E3 (add a room)
class RoomCreate(BaseModel):
    name: str = Field(min_length=1)
    building: str = Field(min_length=1)
    capacity: int = Field(ge=2, le=12)
    has_projector: int = Field(ge=0, le=1)      # 0 = no, 1 = yes

    @field_validator("name", "building")
    @classmethod
    def not_blank(cls, value):
        return clean_text(value)


# E1: Get all the rooms.
def get_all_rooms(min_capacity=None, has_projector=None):
    session = Session(engine)
    query = session.query(rooms)

    if min_capacity is not None:
        query = query.filter(rooms.capacity >= min_capacity)
    if has_projector is not None:
        query = query.filter(rooms.has_projector == has_projector)

    rooms_list = query.all()
    response = []
    for room in rooms_list:
        temp_room = {
            "room_id": room.id,
            "name": room.name,
            "building": room.building,
            "capacity": room.capacity,
            "has_projector": room.has_projector,
            "is_open": room.is_open
        }
        response.append(temp_room)
    session.close()
    return response


# E2: Get one room by id.
def get_room_by_id(room_id):
    session = Session(engine)
    room = session.get(rooms, room_id)

    if room is None:
        session.close()
        raise HTTPException(status_code=404, detail="Room not found")

    response = {
        "room_id": room.id,
        "name": room.name,
        "building": room.building,
        "capacity": room.capacity,
        "has_projector": room.has_projector,
        "is_open": room.is_open,
    }
    session.close()
    return response


# E3: Add a new room.
def add_room(name, building, capacity, has_projector):
    session = Session(engine)
    new_room = rooms(name=name, building=building, capacity=capacity, has_projector=has_projector)
    session.add(new_room)
    session.commit()
    response = {
        "room_id": new_room.id,
        "name": new_room.name,
        "building": new_room.building,
        "capacity": new_room.capacity,
        "has_projector": new_room.has_projector,
        "is_open": new_room.is_open
    }
    session.close()
    return response