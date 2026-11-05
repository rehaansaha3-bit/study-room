from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, date

import Toshimah_functions 
import Harsita_functions 
import Rehaan_functions 

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://127.0.0.1:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)



# E1: Get all the rooms.
@app.get("/rooms")
def get_all_rooms(min_capacity: int = None, has_projector: int = None):
    return Harsita_functions.get_all_rooms(min_capacity, has_projector)


# E2: Get one room by id.
@app.get("/rooms/{room_id}")
def get_room_by_id(room_id):
    return Harsita_functions.get_room_by_id(room_id)


# E3: add a new room.
@app.post("/rooms", status_code=201)
def add_room(name: str, building: str, capacity: int, has_projector: int):
    if name.strip() == "":
        raise HTTPException(status_code=422, detail="Name cannot be empty")
    if building.strip() == "":
        raise HTTPException(status_code=422, detail="Building cannot be empty")
    if capacity < 2 or capacity > 12:
        raise HTTPException(status_code=422, detail="Capacity must be between 2 and 12")
    if has_projector not in [0, 1]:
        raise HTTPException(status_code=422, detail="has_projector must be 0 or 1")
    return Harsita_functions.add_room(name=name, building=building, capacity=capacity, has_projector=has_projector)


# E4 - Open/close room
@app.patch("/rooms/{room_id}")
def update_room(room_id: int, is_open: int):
    if is_open not in [0, 1]:
        raise HTTPException(status_code=422, detail="is_open must be 0 or 1")
    Rehaan_functions.open_close_room(room_id, is_open)
    return {"message": "Room updated"}


# E5 - Get free hours
@app.get("/rooms/{room_id}/free-hours")
def free_hours(room_id: int, booking_date: datetime):
    return Rehaan_functions.get_free_hours(room_id, booking_date)


# E6 book room
@app.post("/rooms/{room_id}/book", status_code=201)
def book_room_endpoint(
    room_id: int,
    booking_date: datetime,
    roll_no: str,
    group_size: int
):
    d = booking_date
    today = datetime.now().date()
    days_away = (d.date() - today).days

    if roll_no.strip() == "":
        raise HTTPException(status_code=422, detail="Roll number cannot be empty")

    if group_size < 1 or group_size > 12:
        raise HTTPException(status_code=422, detail="Group size must be between 1 and 12")

    if days_away < 0:
        raise HTTPException(status_code=422, detail="You can't book a date in the past")

    if days_away > 7:
        raise HTTPException(status_code=422, detail="You can only book up to 7 days from today")

    if d.hour < 8 or d.hour > 19:
        raise HTTPException(status_code=422, detail="Start hour must be between 8 and 19")

    if not roll_no.isdigit():
        raise HTTPException(status_code=400, detail="Roll number must be a number")

    # Save the date at midnight, because the hour goes in start_hour
    midnight = datetime(d.year, d.month, d.day)

    return Rehaan_functions.book_room(room_id, midnight, d.hour, roll_no, group_size)


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
