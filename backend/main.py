from fastapi import FastAPI
from functions import change_room
app = FastAPI()

# E4 - Open/close room
@app.put("/rooms/{room_id}")
def update_room(room_id: int, is_open: bool):
    change_room(room_id, is_open)
    return {"message": "Room updated"}


# E5 - Get free hours
@app.get("/rooms/{room_id}/free-hours")
def free_hours(room_id: int, booking_date: date):
    return get_free_hours(room_id, booking_date)

# E6 book room
@app.post("/rooms/{room_id}/book")
def book(room_id: int, booking_date: date, start_hour: int, roll_no: str, group_size: int):
    book_room(room_id, booking_date, start_hour, roll_no, group_size)
    return {"message": "Room booked"}


