from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime;
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
    roll_no = Column(Integer)
    booking_date = Column(DateTime, default=datetime.now)
    start_hour = Column(Integer)
    group_size = Column(Integer)
    status = Column(String)
    booked_on = Column(DateTime, default=datetime.now)


Base.metadata.create_all(engine)


# E7
# Get one student's bookings that aren't cancelled and are today or later, by roll number.
def student_bookings(roll_no):
    session = Session(engine)
    
    
    if not roll_no.isdigit():
        session.close()
        raise HTTPException(status_code=400, detail="Roll number must be a number")

    roll_no = int(roll_no)
    
    student_booking_records = session.query(bookings).filter(
        bookings.roll_no == roll_no,
        bookings.status != "cancelled",
        bookings.booking_date >= datetime.now()
    ).all()

    if not student_booking_records:
        session.close()
        raise HTTPException(status_code=404, detail="No bookings found for this student")
    
    response = []
    for booking in student_booking_records:
        room = session.get(rooms, booking.room_id)
        response.append({
            "booking_id": booking.id,
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
    if booking_id.isdigit() == False:
        session.close()
        raise HTTPException(status_code=400, detail="Booking ID must be a number")
    booking = session.get(bookings, int(booking_id))
    if not booking:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled" :
        session.close()
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    if booking.status == "checked_in":
        session.close()
        raise HTTPException(status_code=400, detail="Cannot cancel a checked-in booking")
    
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
    if booking_id.isdigit() == False:
        session.close()
        raise HTTPException(status_code=400, detail="Booking ID must be a number")
    booking = session.get(bookings, int(booking_id))
    if not booking:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.status == "cancelled":
        session.close()
        raise HTTPException(status_code=400, detail="Cannot check in to a cancelled booking")
    if booking.status == "checked_in":
        session.close()
        raise HTTPException(status_code=400, detail="Already checked in")
    if booking.booking_date.date() != datetime.now().date():
        session.close()
        raise HTTPException(status_code=400, detail="Can only check in on the booking date")
    
    booking.status = "checked_in"
    
    room = session.get(rooms, booking.room_id)
    if room:
        room.is_open = 0
        
    session.commit()
    session.close()
    return {"detail": "Checked in successfully"} 

# E10
# get all bookings
def get_all_bookings():
    session = Session(engine)
    booking_list = session.query(bookings).all()
    response = []
    for booking in booking_list:
        temp_booking = {
            "booking_id": booking.id,
            "room_id": booking.room_id,
            "roll_no": booking.roll_no,
            "status": booking.status,
            "booking_date": booking.booking_date,
            "start_hour": booking.start_hour,
            "group_size": booking.group_size,
            "booked_on": booking.booked_on
        }
        response.append(temp_booking)
    session.close()
    return response