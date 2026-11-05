import { useState } from "react";

function RoomItem({ room, changeRoomStatus }) {
    return (
        <div>
            <hr />

            <h3>{room.name}</h3>
            <p>Building: {room.building}</p>
            <p>Capacity: {room.capacity}</p>
            <p>Projector: {room.has_projector == 1 ? "Yes" : "No"}</p>
            <p>Status: {room.is_open == 1 ? "Open" : "Closed"}</p>

            <button onClick={() => changeRoomStatus(room)}>
                {room.is_open == 1 ? "Close Room" : "Open Room"}
            </button>
        </div>
    );
}


function ManageRooms({ rooms, message, addRoom, changeRoomStatus }) {

    const [name, setName] = useState("");
    const [building, setBuilding] = useState("");
    const [capacity, setCapacity] = useState("");
    const [projector, setProjector] = useState("0");

    return (
        <>
            <h1>Manage Rooms</h1>

            <h2>Add a Room</h2>

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

            <select
                value={projector}
                onChange={(e) => setProjector(e.target.value)}
            >
                <option value="0">No Projector</option>
                <option value="1">Has Projector</option>
            </select>

            <button onClick={() => {
                addRoom(name, building, capacity, Number(projector));

                setName("");
                setBuilding("");
                setCapacity("");
                setProjector("0");
            }}>
                Add Room
            </button>

            <p>{message}</p>

            <h2>All Rooms</h2>

            {rooms.map((room) => (
                <RoomItem
                    key={room.room_id}
                    room={room}
                    toggleRoom={toggleRoom}
                />
            ))}
        </>
    );
}

export default ManageRooms;



