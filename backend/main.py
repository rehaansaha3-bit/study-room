from fastapi import FastAPI, HTTPException, Header, Body
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date
import Toshimah_functions 
import Harsita_functions 
from Harsita_functions import RoomCreate
import Rehaan_functions 
from Rehaan_functions import BookingCreate

app = FastAPI()
ROLES = ["student", "staff"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def authorize(token, allowed_roles):
    
    
    payload = Toshimah_functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return payload



# E1: Get all the rooms.
@app.get("/rooms")
def get_all_rooms(min_capacity: int = None, has_projector: int = None, token = Header(None)):
    authorize(token, ["student", "staff"]) 
    return Harsita_functions.get_all_rooms(min_capacity, has_projector)


# E2: Get one room by id.
@app.get("/rooms/{room_id}")
def get_room_by_id(room_id:int , token = Header(None)):
    authorize(token, ["student", "staff"]) 
    return Harsita_functions.get_room_by_id(room_id)


# E3: add a new room.
@app.post("/rooms", status_code=201)
def add_room(room: RoomCreate, token = Header(None)):
    authorize(token, ["staff"]) 
    return Harsita_functions.add_room(name=room.name, building=room.building, capacity=room.capacity, has_projector=room.has_projector)


# E4 - Open/close room
@app.patch("/rooms/{room_id}")
def update_room(room_id: int, is_open: int, token = Header(None)):
    authorize(token, ["staff"]) 
    if is_open not in [0, 1]:
        raise HTTPException(status_code=422, detail="is_open must be 0 or 1")
    Rehaan_functions.open_close_room(room_id, is_open)
    return {"message": "Room updated"}


# E5 - Get free hours
@app.get("/rooms/{room_id}/free-hours")
def free_hours(room_id: int, booking_date: datetime, token = Header(None)):
    authorize(token, ["student"]) 
    return Rehaan_functions.get_free_hours(room_id, booking_date)


# E6 book room
@app.post("/rooms/{room_id}/book", status_code=201)
def book_room_endpoint(room_id: int, booking: BookingCreate, token = Header(None)):
    authorize(token, ["student"])
    d = booking.booking_date

    # Save the date at midnight, because the hour goes in start_hour
    midnight = datetime(d.year, d.month, d.day)
    return Rehaan_functions.book_room(room_id, midnight, d.hour, booking.roll_no, booking.group_size)


# E7
@app.get("/student-bookings/{roll_no}")
def get_student_bookings(roll_no, token = Header(None)):
    authorize(token, ["student","staff"]) 
    return Toshimah_functions.student_bookings(roll_no)

# E8
@app.patch("/cancel-booking/{booking_id}")
def cancel_student_booking(booking_id, token = Header(None)):
    authorize(token, ["student"]) 
    return Toshimah_functions.cancel_booking(booking_id)

# E9
@app.patch("/check-in-booking/{booking_id}")
def check_in_student_booking(booking_id, token = Header(None)):
    authorize(token, ["student"]) 
    return Toshimah_functions.check_in_booking(booking_id)


# E10
@app.get("/bookings")
def get_all_bookings(token = Header(None)):
    authorize(token, ["staff"]) 
    return Toshimah_functions.get_all_bookings()

@app.post("/login")
def login(username= Body(), password= Body()):
    token =  Toshimah_functions.verify_login(username = username, password=password)
    if not token  :
        raise HTTPException(status_code = 401, detail="Invalid credentials")
    payload = Toshimah_functions.verify_token(token=token["access_token"], token_type="access")
    token["role"] = payload["role"]
    return token

@app.post("/refresh")
def refresh(refresh_token = Header(None)):
   payload = Toshimah_functions.verify_token(token=refresh_token, token_type="refresh")
   if not payload:
       raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")
   
   access_token = Toshimah_functions.create_token(username=payload["username"], token_type= "access", user_id= payload["user_id"] , role=payload["role"])
   return {"access_token" : access_token}

@app.post("/register")
def register_user(user_name= Body(), password = Body(), role = Body("student")):
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="Role must be student or staff")
    if Toshimah_functions.register_user(user_name=user_name, password=password, role=role):
        return {"message": "user registered successfully"}
    raise HTTPException(status_code=400, detail="User already exists")
   