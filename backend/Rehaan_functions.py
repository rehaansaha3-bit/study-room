from contextlib import closing

from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime;
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
    booking_date = Column(DateTime, default=datetime.now)
    start_hour = Column(Integer)
    group_size = Column(Integer)
    status = Column(String)
    booked_on = Column(DateTime, default=datetime.now)


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
            # bookings.booking_date >= datetime.now(),
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
        bookings.booking_date == booking_date,
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
def book_room(room_id, booking_date, start_hour, roll_no, group_size):
    session = Session(engine)
    room = session.get(rooms, room_id)

    if not room:
        session.close()
        raise HTTPException(status_code=404, detail="Room not found")

    if not room.is_open:
        session.close()
        raise HTTPException(status_code=400, detail="Room is closed for booking")
    
    if start_hour < 8 or start_hour > 19:
        session.close()
        raise HTTPException(status_code=400, detail="Start hour must be between 8 and 19")
    
    
    if group_size > room.capacity:
        session.close()
        raise HTTPException(status_code=400, detail="Group size exceeds room capacity")

    
    new_booking = bookings(
        room_id=room_id,
        booking_date=booking_date,
        start_hour=start_hour,
        roll_no=roll_no,
        group_size=group_size,
        status="booked"
    )

    session.add(new_booking)
    session.commit()
    session.close()