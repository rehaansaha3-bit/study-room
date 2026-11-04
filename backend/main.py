from fastapi import FastAPI, HTTPException
from datetime import datetime, date
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
def add_room( name:str, building:str, capacity:int, has_projector:int):
    # if name.strip() == "" or name.strip().isdigit() :
    #     raise HTTPException(status_code=400, detail="Name cannot be empty or a number")
    # if building.strip() == "" or building.strip().isdigit() :
    #     raise HTTPException(status_code=400, detail="Building cannot be empty or a number")
    if capacity <= 0:
        raise HTTPException(status_code=400, detail="Capacity must be a positive number")
    if has_projector not in [0, 1]:
            raise HTTPException(status_code=400, detail="has_projector must be 0 or 1")
    return Harsita_functions.add_room( name = name, building = building, capacity = capacity, has_projector = has_projector)


# E4 - Open/close room
@app.patch("/rooms/{room_id}")
def update_room(room_id: int, is_open: int):
    if is_open not in [0, 1]:
        raise HTTPException(status_code=400, detail="is_open must be 0 or 1")
    Rehaan_functions.open_close_room(room_id, is_open)
    return {"message": "Room updated"}


# E5 - Get free hours
@app.get("/rooms/{room_id}/free-hours")
def free_hours(room_id: int):
    return Rehaan_functions.get_free_hours(room_id, date.today())

# E6 book room
@app.post("/rooms/{room_id}/book")
def book_room_endpoint(
    room_id: int, 
    booking_date: datetime,  # FastAPI automatically converts the string to a datetime object!
    start_hour: int, 
    roll_no: str, 
    group_size: int
):
    if not roll_no.isdigit():
        raise HTTPException(status_code=400, detail="Roll number must be a number")
    
    if start_hour < 8 or start_hour > 19:
        raise HTTPException(status_code=400, detail="Start hour must be between 8 and 19")
    
    return Rehaan_functions.book_room(
        room_id, 
        booking_date.date(),  # Extracts just the date (e.g., 2026-11-06)
        start_hour, 
        roll_no, 
        group_size
    )


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
    
