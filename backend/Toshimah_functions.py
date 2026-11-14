from sqlalchemy import Integer, String, Column, create_engine,ForeignKey, DateTime
from sqlalchemy.orm import Session, declarative_base;
from datetime import datetime, timezone, timedelta;
from fastapi import HTTPException;
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "study_room.db"

USERNAME = "Toshimah"
PASSWORD = "123456789"
ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7 * 24 * 60
SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

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
        bookings.booking_date >= datetime.now().date()
    ).all()

    response = []
    for booking in student_booking_records:
        room = session.get(rooms, booking.room_id)
        response.append({
            "booking_id": booking.id,
            "room_name": room.name if room else None,
            "booking_date": booking.booking_date.date(),
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
    session.commit()
    session.close()
    return {"message": "Booking cancelled successfully"}

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
    session.commit()
    session.close()
    return {"message": "Checked in successfully"}

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

def verify_login(username, password):
    session = Session(engine)
    user = session.query(Users).filter_by(user_name= username).first()
    if user is None:
        session.close()
        return False
    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        session.close()
        return False

    access_token = create_token(username=username,token_type="access",user_id=user.user_id,role=user.role,)
    refresh_token = create_token(username=username,token_type="refresh",user_id=user.user_id,role=user.role,)

    session.close()
    return {"access_token": access_token, "refresh_token": refresh_token}


def create_token(username, token_type, user_id, role):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {
        "user_id": user_id,
        "role": role,
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time),
    }
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return False
    if payload["token_type"] == token_type:
        return payload
    return False


#--------------Users-------------------
def register_user(user_name :str, password: str, role: str):
    session = Session(engine)
    user_exists = session.query(Users).filter_by(user_name = user_name).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(Users(user_name=user_name, password=hashed_password, role=role))
    session.commit()
    session.close()
    return True