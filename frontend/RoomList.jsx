import RoomItem from "./RoomItem";

function RoomList({ rooms, onAdd }) {
  return (
    <>
      <h1>Rooms</h1>
      <ul className="room-list">
        {rooms.map((room) => (
          <RoomItem key={room.id} room={room} onAdd={onAdd} />
        ))}
      </ul>
    </>
  );
}

export default RoomList;