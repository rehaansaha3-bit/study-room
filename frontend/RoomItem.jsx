
function RoomItem({ room, onAdd }) {
  return (
    <li className="room">
      <h2>{room.name}</h2>
      <p>{room.description}</p>
      <p>₹{room.price}</p>

      {room.available ? (
        <button onClick={() => onAdd(room.id)}>Add to cart</button>
      ) : (
        <p>Sold out</p>
      )}
    </li>
  );
}

export default RoomItem;