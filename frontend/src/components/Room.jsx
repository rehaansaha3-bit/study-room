import { useEffect, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import RoomItem from "./RoomItem";

// Turns a date into text like 2026-11-05
function formatDate(d) {
  // The date is null when someone clears the box
  if (d === null) {
    return "";
  }

  let month = d.getMonth() + 1;
  let day = d.getDate();

  if (month < 10) {
    month = "0" + month;
  }
  if (day < 10) {
    day = "0" + day;
  }

  return d.getFullYear() + "-" + month + "-" + day;
}

function Rooms({ apiUrl, refresh, onChange }) {
  // Today, and the last date a student can book (7 days from today)
  const today = new Date();
  const lastDate = new Date();
  lastDate.setDate(lastDate.getDate() + 7);

  const [rooms, setRooms] = useState([]);
  const [minCapacity, setMinCapacity] = useState("");
  const [projectorOnly, setProjectorOnly] = useState(false);
  const [startDate, setStartDate] = useState(new Date());
  const [selectedRoomId, setSelectedRoomId] = useState(null);

  // E1: load all rooms
  useEffect(() => {
    fetch(apiUrl + "/rooms")
      .then((response) => response.json())
      .then((data) => setRooms(data));
  }, [refresh]);

  // E2: get the room that was clicked
  function handleSelect(roomId) {
    fetch(apiUrl + "/rooms/" + roomId)
      .then((response) => response.json())
      .then(() => setSelectedRoomId(roomId));
  }

  const filteredRooms = rooms.filter((room) => {
    if (projectorOnly && !room.has_projector) {
      return false;
    }
    return true;
  });

  return (
    <section>
      <h2>Rooms</h2>


      <label>
        <input
          type="checkbox"
          checked={projectorOnly}
          onChange={(e) => setProjectorOnly(e.target.checked)}
        />
        Has projector
      </label>

      <DatePicker
        selected={startDate}
        onChange={(date) => setStartDate(date)}
        minDate={today}
        maxDate={lastDate}
        dateFormat="yyyy-MM-dd"
      />

      <ul>
        {filteredRooms.map((room) => (
          <RoomItem
            key={room.room_id}
            room={room}
            apiUrl={apiUrl}
            date={formatDate(startDate)}
            isSelected={selectedRoomId === room.room_id}
            onSelect={handleSelect}
            refresh={refresh}
            onChange={onChange}
          />
        ))}
      </ul>
    </section>
  );
}

export default Rooms;