from fastapi import FastAPI, HTTPException
from datetime import datetime 
import Toshimah_functions 
import Harsita_functions 
import Rehaan_functions 

app = FastAPI()


# E1: Get all the rooms.
@app.get("/rooms")
def get_all_rooms():
    return Harsita_functions.get_all_rooms()


# E2: Get one room by id.
@app.get("/rooms/{room_id}")
def get_room_by_id(room_id):
    return Harsita_functions.get_room_by_id(room_id)

# E3: add a new room.
@app.post("/rooms")
def add_room( name, building, capacity, has_projector):
    if name.strip()=="" or name.strip().isdigit() or building.strip()=="" or building.strip().isdigit():
        raise HTTPException(status_code=400, detail="Name and building cannot be empty")
    return Harsita_functions.add_room( name = name, building = building, capacity = capacity, has_projector = has_projector)


# E4 - Open/close room
@app.patch("/rooms/{room_id}")
def update_room(room_id, is_open):
    if is_open not in [0, 1]:
        raise HTTPException(status_code=400, detail="is_open must be 0 or 1")
    Rehaan_functions.open_close_room(room_id, is_open)
    return {"message": "Room updated"}


# E5 - Get free hours
@app.get("/rooms/{room_id}/free-hours")
def free_hours(room_id):
    return Rehaan_functions.get_free_hours(room_id, datetime.now())

# E6 book room
@app.post("/rooms/{room_id}/book")
def book(room_id, start_hour, roll_no, group_size):
    Rehaan_functions.book_room(room_id, datetime.now(), start_hour, roll_no, group_size)
    return {"message": "Room booked"}


# E7
@app.get("/student-bookings/{roll_no}")
def get_student_bookings(roll_no):
    return Toshimah_functions.student_bookings(roll_no)

# E8
@app.patch("/cancel-booking/{booking_id}")
def cancel_student_booking(booking_id):
    return Toshimah_functions.cancel_booking(booking_id)

# E9
@app.patch("/check-in-booking/{booking_id}")
def check_in_student_booking(booking_id):
    return Toshimah_functions.check_in_booking(booking_id)


# E10
@app.get("/bookings")
def get_all_bookings():
    return Toshimah_functions.get_all_bookings()
    
