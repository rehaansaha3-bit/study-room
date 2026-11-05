import { useState } from "react";
import Rooms from "./components/Room";
import MyBooking from "./components/MyBooking";
import ManageRooms from "./components/ManageRooms";

const API_URL = "http://127.0.0.1:8001";

function App() {
  // When this number changes, every part of the page loads its data again
  const [refresh, setRefresh] = useState(0);

  function updatePage() {
    setRefresh(refresh + 1);
  }

  return (
    <div>
      <h1>Study Room Booking</h1>
      <Rooms apiUrl={API_URL} refresh={refresh} onChange={updatePage} />
      <hr />
      <MyBooking apiUrl={API_URL} refresh={refresh} onChange={updatePage} />
      <hr />
      <ManageRooms apiUrl={API_URL} refresh={refresh} onChange={updatePage} />
    </div>
  );
}

export default App;