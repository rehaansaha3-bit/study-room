from contextlib import closing

from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import date;
from fastapi import HTTPException;
import Harsita_functions 

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
    booking_date = Column(DateTime )
    start_hour = Column(Integer)
    group_size = Column(Integer)
    status = Column(String)
    booked_on = Column(DateTime, default= date.today())


Base.metadata.create_all(engine)

# E4 E5 E6

# E4: 
def open_close_room(room_id, is_open):
    session = Session(engine)
    room = session.get(rooms, room_id)

    # closing a room that has future bookings should not be allowed.
    if not is_open:
        future_bookings = session.query(bookings).filter(
            bookings.room_id == room_id,
            bookings.booking_date >=  bookings.booking_date.strftime("%Y-%m-%d %H:%M:%S"),
            bookings.status != "cancelled"
        ).all()

        if future_bookings:
            session.close()
            raise HTTPException(status_code=400, detail="Cannot close room with future bookings")
    
    if room:
        room.is_open = is_open
        session.commit()

    session.close()

# E5:
def get_free_hours(room_id, booking_date):
    session = Session(engine)

    booking = session.query(bookings).filter(
        bookings.room_id == room_id,
        bookings.booking_date == booking_date.strftime("%Y-%m-%d %H:%M:%S"),
        bookings.status != "cancelled"
    ).all()

    booked_hours = []

    for b in booking:
        booked_hours.append(b.start_hour)

    free_hours = []

    for hour in range(8, 20):
        if hour not in booked_hours:
            free_hours.append(hour)

    session.close()
    return free_hours

# E6:
def book_room(room_id: int, booking_date: date, start_hour: int, roll_no: str, group_size: int):
    session = Session(engine)

    room = session.get(rooms, room_id)
    if not room:
        session.close()
        raise HTTPException(status_code=404, detail="Room not found")

    if not room.is_open:
        session.close()
        raise HTTPException(status_code=400, detail="Room is closed for booking")
    
    if group_size > room.capacity:
        session.close()
        raise HTTPException(status_code=400, detail="Group size exceeds room capacity")

    existing_booking = session.query(bookings).filter(
        bookings.room_id == room_id,
        bookings.booking_date == booking_date,
        bookings.start_hour == start_hour,
        bookings.status != "cancelled"
    ).first()
    
    if existing_booking:
        session.close()
        raise HTTPException(status_code=400, detail="Room is already booked for this hour")

    new_booking = bookings(
        room_id=room_id,
        booking_date=booking_date,      
        start_hour=start_hour,
        roll_no=int(roll_no),
        group_size=group_size,
        status="booked",
        booked_on=date.today()         
    )

    session.add(new_booking)
    session.commit()
    session.close()
    
    return {"message": "Room booked successfully"}