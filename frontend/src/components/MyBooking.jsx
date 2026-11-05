import { useEffect, useState } from "react";

function getErrorMessage(data) {
  if (typeof data.detail === "string") {
    return data.detail;
  }
  return "Please check what you typed.";
}

function MyBooking({ apiUrl, refresh, onChange }) {
  const [bookings, setBookings] = useState([]);
  const [rollNumber, setRollNumber] = useState("");
  const [error, setError] = useState("");

  // E7: get the student's bookings
  function getBookings() {
    fetch(apiUrl + "/student-bookings/" + rollNumber)
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setBookings([]);
          setError(getErrorMessage(data));
        } else {
          setBookings(data);
        }
      });
  }

  function handleShow() {
    setError("");
    getBookings();
  }

  // Load the list again after a booking, check-in or cancel
  useEffect(() => {
    if (rollNumber !== "") {
      getBookings();
    }
  }, [refresh]);

  // E9: check in
  function handleCheckIn(bookingId) {
    setError("");

    fetch(apiUrl + "/check-in-booking/" + bookingId, { method: "PATCH" })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setError(getErrorMessage(data));
        } else {
          onChange();
        }
      });
  }

  // E8: cancel
  function handleCancel(bookingId) {
    setError("");

    fetch(apiUrl + "/cancel-booking/" + bookingId, { method: "PATCH" })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setError(getErrorMessage(data));
        } else {
          onChange();
        }
      });
  }

  return (
    <section>
      <h2>My Bookings</h2>

      <input
        placeholder="Roll number"
        value={rollNumber}
        onChange={(e) => setRollNumber(e.target.value)}
      />
      <button onClick={handleShow}>Show</button>

      {error !== "" && <p>{error}</p>}

      <ul>
        {bookings.map((booking) => (
          <li key={booking.booking_id}>
            <h3>{booking.room_name}</h3>
            <p>Date: {booking.booking_date}</p>
            <p>Time: {booking.start_hour}:00</p>

            <button onClick={() => handleCheckIn(booking.booking_id)}>
              Check In
            </button>
            <button onClick={() => handleCancel(booking.booking_id)}>
              Cancel
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default MyBooking;
