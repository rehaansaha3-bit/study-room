from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import date;
from fastapi import HTTPException;

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
    roll_no = Column(String)
    booking_date = Column(DateTime)
    start_hour = Column(Integer)
    group_size = Column(Integer)
    status = Column(String)
    booked_on = Column(DateTime)


Base.metadata.create_all(engine)


# E7
# Get one student's bookings that aren't cancelled and are today or later, by roll number. Each one includes the room's name.


def student_bookings(roll_no):
    session = Session(engine)
    student_booking_records = session.get(
            bookings.roll_no == roll_no,
            bookings.status != "cancelled",
            bookings.booking_date >= date.today()
        )
    if not student_booking_records:
        session.close()
        raise HTTPException(status_code=404, detail="No bookings found for this student")
    
    response = []
    for booking in student_booking_records:
        room = session.get(rooms, booking.room_id)
        response.append({
            "id": booking.id,
            "room_name": room.name if room else None,
            "booking_date": booking.booking_date,
            "start_hour": booking.start_hour,
            "group_size": booking.group_size
        })
    session.close()
    return response
       
       
# E8
# Cancel a booking.

def cancel_booking(booking_id):
    session = Session(engine)
    booking = session.get(bookings, booking_id)
    if not booking:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        session.close()
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    
    booking.status = "cancelled"
    
    room = session.get(rooms, booking.room_id)
    if room:
        room.is_open = 1
        
    session.commit()
    session.close()
    return {"detail": "Booking cancelled successfully"} 

# E9
# Check in to a booking.

def check_in_booking(booking_id):
    session = Session(engine)
    booking = session.get(bookings, booking_id)
    if not booking:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        session.close()
        raise HTTPException(status_code=400, detail="Cannot check in to a cancelled booking")
    if booking.status == "checked_in":
        session.close()
        raise HTTPException(status_code=400, detail="Already checked in")
    
    booking.status = "checked_in"
    
    room = session.get(rooms, booking.room_id)
    if room:
        room.is_open = 0
        
    session.commit()
    session.close()
    return {"detail": "Checked in successfully"} 