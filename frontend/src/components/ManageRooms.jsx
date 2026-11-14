import { useEffect, useState } from "react";

function getErrorMessage(data) {
  if (typeof data.detail === "string") {
    return data.detail;
  }
  // Pydantic errors (422) come as a list
  if (Array.isArray(data.detail) && data.detail.length > 0) {
    return data.detail[0].msg.replace("Value error, ", "");
  }
  return "Please check what you typed.";
}

function ManageRooms({ apiUrl, token, refresh, onChange }) {
  const [rooms, setRooms] = useState([]);
  const [name, setName] = useState("");
  const [building, setBuilding] = useState("");
  const [capacity, setCapacity] = useState("");
  const [projector, setProjector] = useState("0");
  const [message, setMessage] = useState("");

  // E1: load all rooms
  useEffect(() => {
    fetch(apiUrl + "/rooms", { headers: { token: token } })
      .then((response) => response.json())
      .then((data) => {
        if (!data.detail) {
          setRooms(data);
        }
      });
  }, [refresh]);

  // E3: add a new room (RoomCreate expects a JSON body)
  function handleAdd() {
    setMessage("");

    fetch(apiUrl + "/rooms", {
      method: "POST",
      headers: { "Content-Type": "application/json", token: token },
      body: JSON.stringify({
        name: name,
        building: building,
        capacity: Number(capacity),
        has_projector: Number(projector),
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(getErrorMessage(data));
        } else {
          setMessage("Room added!");
          setName("");
          setBuilding("");
          setCapacity("");
          setProjector("0");
          onChange();
        }
      });
  }

  // E4: open or close a room (is_open is a query parameter)
  function handleStatus(room) {
    setMessage("");
    const newStatus = room.is_open ? 0 : 1;

    fetch(apiUrl + "/rooms/" + room.room_id + "?is_open=" + newStatus, {
      method: "PATCH",
      headers: { token: token },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(getErrorMessage(data));
        } else {
          onChange();
        }
      });
  }

  return (
    <section>
      <h2>Manage Rooms</h2>

      <input placeholder="Room name" value={name} onChange={(e) => setName(e.target.value)} />
      <input
        placeholder="Building"
        value={building}
        onChange={(e) => setBuilding(e.target.value)}
      />
      <input
        type="number"
        placeholder="Capacity"
        value={capacity}
        onChange={(e) => setCapacity(e.target.value)}
      />
      <select value={projector} onChange={(e) => setProjector(e.target.value)}>
        <option value="0">No projector</option>
        <option value="1">Has projector</option>
      </select>
      <button onClick={handleAdd}>Add Room</button>

      {message !== "" && <p>{message}</p>}

      <ul>
        {rooms.map((room) => (
          <li key={room.room_id}>
            {room.name} - {room.is_open ? "Open" : "Closed"}
            <button onClick={() => handleStatus(room)}>{room.is_open ? "Close" : "Open"}</button>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default ManageRooms;