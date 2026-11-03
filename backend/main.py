from fastapi import FastAPI, HTTPException
import Toshimah_functions 

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