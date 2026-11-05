import { useEffect, useState } from "react";

function RoomItem({ room, apiUrl, date, isSelected, onSelect, refresh, onChange }) {
  const [freeHours, setFreeHours] = useState([]);
  const [rollNo, setRollNo] = useState("");
  const [groupSize, setGroupSize] = useState("");
  const [error, setError] = useState("");

  // E5: load the free hours
  useEffect(() => {
    if (!isSelected || date === "") {
      return;
    }

    fetch(apiUrl + "/rooms/" + room.room_id + "/free-hours?booking_date=" + date)
      .then((response) => response.json())
      .then((data) => setFreeHours(data));
  }, [isSelected, date, refresh]);

  // E6: book one free hour
function handleBook(hour) {
  setError("");

  // The backend reads the hour from the date, like 2026-11-05T09:00:00
  let hourText = hour;
  if (hour < 10) {
    hourText = "0" + hour;
  }
  const bookingDate = date + "T" + hourText + ":00:00";

  let url = apiUrl + "/rooms/" + room.room_id + "/book";
  url = url + "?booking_date=" + bookingDate;
  url = url + "&roll_no=" + rollNo;
  url = url + "&group_size=" + groupSize;

  fetch(url, { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      if (typeof data.detail === "string") {
        setError(data.detail);
      } else if (data.detail) {
        setError("Please check what you typed.");
      } else {
        onChange();
      }
    });
}

  return (
    <li>
      <button onClick={() => onSelect(room.room_id)}>{room.name}</button>
      <p>Building: {room.building}</p>
      <p>Capacity: {room.capacity}</p>
      <p>Projector: {room.has_projector ? "Yes" : "No"}</p>
      {!room.is_open && <p>Closed</p>}

      {isSelected && (
        <div>
          <h3>Free hours on {date}</h3>

          <input
            placeholder="Roll number"
            value={rollNo}
            onChange={(e) => setRollNo(e.target.value)}
          />
          <input
            type="number"
            placeholder="Group size"
            value={groupSize}
            onChange={(e) => setGroupSize(e.target.value)}
          />

          <p>{error}</p>

          {freeHours.map((hour) => (
            <p key={hour}>
              {hour}:00 - {hour + 1}:00
              <button onClick={() => handleBook(hour)}>Book</button>
            </p>
          ))}
        </div>
      )}
    </li>
  );
}

export default RoomItem;