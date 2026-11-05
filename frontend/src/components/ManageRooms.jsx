
import { useEffect, useState } from "react";

function ManageRooms({ apiUrl }) {

    const [rooms, setRooms] = useState([]);
    const [name, setName] = useState("");
    const [building, setBuilding] = useState("");
    const [capacity, setCapacity] = useState("");
    const [projector, setProjector] = useState("0");
    const [message, setMessage] = useState("");

    // E1: Get all rooms
    function getRooms() {
        fetch(apiUrl + "/rooms")
            .then(res => res.json())
            .then(data => setRooms(data));
    }

    useEffect(() => {
        getRooms();
    }, []);

    // E3: Add a room
    function addRoom() {

        let url = apiUrl + "/rooms?name=" + encodeURIComponent(name);
        url = url + "&building=" + encodeURIComponent(building);
        url = url + "&capacity=" + capacity;
        url = url + "&has_projector=" + projector;

        fetch(url, { method: "POST" })
            .then(res => res.json())
            .then(data => {
                if (data.detail) {
                    setMessage(data.detail);
                }
                else {
                    setMessage("Room added!");
                    setName("");
                    setBuilding("");
                    setCapacity("");
                    setProjector("0");
                    getRooms();
                }
            });
    }

    // E4: Open or close room
    function openCloseRoom(room) {

        let status = room.is_open ? 0 : 1;

        fetch(apiUrl + "/rooms/" + room.room_id + "?is_open=" + status, {
            method: "PATCH"
        })
            .then(res => res.json())
            .then(data => {
                if (data.detail) {
                    setMessage(data.detail);
                }
                else {
                    setMessage("Room updated!");
                    getRooms();
                }
            });
    }

    return (
        <>
            <h2>Manage Rooms</h2>

            <h3>Add Room</h3>

            <input
                placeholder="Room name"
                value={name}
                onChange={(e) => setName(e.target.value)}
            />

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
                <option value="0">No Projector</option>
                <option value="1">Has Projector</option>
            </select>

            <button onClick={addRoom}>Add Room</button>

            <p>{message}</p>

            <h3>All Rooms</h3>

            {rooms.map((room) => (
                <div key={room.room_id}>
                    <h4>{room.name}</h4>
                    <p>Building: {room.building}</p>
                    <p>Capacity: {room.capacity}</p>
                    <p>Projector: {room.has_projector == 1 ? "Yes" : "No"}</p>
                    <p>Status: {room.is_open == 1 ? "Open" : "Closed"}</p>

                    <button onClick={() => openCloseRoom(room)}>
                        {room.is_open == 1 ? "Close Room" : "Open Room"}
                    </button>
                </div>
            ))}
        </>
    );
}

export default ManageRooms;
