from fastapi import FastAPI, HTTPException
import Toshimah_functions 
import Harsita_functions 

app = FastAPI()

@app.get("/student-bookings/{roll_no}")
def get_student_bookings(roll_no):
    return Toshimah_functions.student_bookings(roll_no)

@app.patch("/cancel-booking/{booking_id}")
def cancel_student_booking(booking_id):
    return Toshimah_functions.cancel_booking(booking_id)

@app.patch("/check-in-booking/{booking_id}")
def check_in_student_booking(booking_id):
    return Toshimah_functions.check_in_booking(booking_id)




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
    return Harsita_functions.add_room( name = name, building = building, capacity = capacity, has_projector = has_projector)
