# E4 E5 E6

# E4: 
def open_close_room(room_id, is_open):
    session = Session(engine)
    room = session.get(Room, room_id)

    if room:
        room.is_open = is_open
        session.commit()

    session.close()

# E5:
def get_free_hours(room_id, booking_date):
    session = Session(engine)

    bookings = session.query(Booking).filter(
        Booking.room_id == room_id,
        Booking.booking_date == booking_date,
        Booking.status != "cancelled"
    ).all()

    booked_hours = []

    for b in bookings:
        booked_hours.append(b.start_hour)

    free_hours = []

    for hour in range(8, 20):
        if hour not in booked_hours:
            free_hours.append(hour)

    session.close()
    return free_hours

# E6:
def book_room(room_id, booking_date, start_hour, roll_no, group_size):
    session = Session(engine)

    new_booking = Booking(
        room_id=room_id,
        booking_date=booking_date,
        start_hour=start_hour,
        roll_no=roll_no,
        group_size=group_size,
        status="booked"
    )

    session.add(new_booking)
    session.commit()
    session.close()


