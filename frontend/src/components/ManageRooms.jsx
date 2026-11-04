import React, { useState, useEffect } from "react";
import { API_URL } from "../api";

function ManageRooms() {

    const [rooms, setRooms] = useState([]);
    const [message, setMessage] = useState("");

    const [name, setName] = useState("");
    const [building, setBuilding] = useState("");
    const [capacity, setCapacity] = useState("");
    const [hasProjector, setHasProjector] = useState("0");


    // Get all rooms
    async function getRooms() {
        try {
            const response = await fetch(`${API_URL}/rooms`);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }

            setRooms(data);
        } 
        catch (error) {
            setMessage(error.message);
        }
    }


    // Load rooms when the page opens
    useEffect(() => {
        getRooms();
    }, []);


    // Add a new room
    async function addRoom(e) {
        e.preventDefault();
        setMessage("");

        try {
            const params = new URLSearchParams({
                name: name,
                building: building,
                capacity: capacity,
                has_projector: hasProjector
            });

            const response = await fetch(
                `${API_URL}/rooms?${params}`,
                { method: "POST" }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }

            setMessage("Room added successfully!");

            // Clear the form
            setName("");
            setBuilding("");
            setCapacity("");
            setHasProjector("0");

            // Update the room list
            getRooms();

        } 
        catch (error) {
            setMessage(error.message);
        }
    }


    // Open or close a room
    async function toggleRoom(room) {
        setMessage("");

        const newStatus = room.is_open === 1 ? 0 : 1;

        try {
            const response = await fetch(
                `${API_URL}/rooms/${room.room_id}?is_open=${newStatus}`,
                { method: "PATCH" }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }

            setMessage("Room updated successfully!");

            // Update the room list
            getRooms();

        } 
        catch (error) {
            setMessage(error.message);
        }
    }


    return (
        <div>

            <h2>Manage Rooms</h2>

            {/* Add Room Form */}
            <h3>Add a New Room</h3>

            <form onSubmit={addRoom}>

                <input
                    type="text"
                    placeholder="Room Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required
                />

                <input
                    type="text"
                    placeholder="Building"
                    value={building}
                    onChange={(e) => setBuilding(e.target.value)}
                    required
                />

                <input
                    type="number"
                    placeholder="Capacity"
                    min="2"
                    max="12"
                    value={capacity}
                    onChange={(e) => setCapacity(e.target.value)}
                    required
                />

                <select
                    value={hasProjector}
                    onChange={(e) => setHasProjector(e.target.value)}
                >
                    <option value="0">No Projector</option>
                    <option value="1">Has Projector</option>
                </select>

                <button type="submit">
                    Add Room
                </button>

            </form>


            {/* Success or Error Message */}
            {message && (
                <p>{message}</p>
            )}


            {/* Display All Rooms */}
            <h3>All Rooms</h3>

            {rooms.map((room) => (

                <div key={room.room_id}>

                    <h4>{room.name}</h4>

                    <p>Building: {room.building}</p>

                    <p>Capacity: {room.capacity}</p>

                    <p>
                        Projector: {room.has_projector === 1 ? "Yes" : "No"}
                    </p>

                    <p>
                        Status: {room.is_open === 1 ? "Open" : "Closed"}
                    </p>

                    <button onClick={() => toggleRoom(room)}>
                        {room.is_open === 1 ? "Close Room" : "Open Room"}
                    </button>

                    <hr />

                </div>

            ))}

        </div>
    );
}

export default ManageRooms;