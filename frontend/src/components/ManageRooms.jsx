import { useState } from "react";

function RoomItem({ room, toggleRoom }) {    
    // shows statusof room
    return (
        <div>
            <hr />

            <h3>{room.name}</h3>
            <p>Building: {room.building}</p>
            <p>Capacity: {room.capacity}</p>
            <p>Projector: {room.has_projector == 1 ? "Yes" : "No"}</p>
            <p>Status: {room.is_open == 1 ? "Open" : "Closed"}</p>

            <button onClick={() => toggleRoom(room)}>
                {room.is_open == 1 ? "Close Room" : "Open Room"}
            </button>
        </div>
    );
}


