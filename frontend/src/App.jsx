import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Rooms from "./components/Room";
import MyBooking from "./components/MyBooking";
import ManageRooms from "./components/ManageRooms";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [token, setToken] = useState("");
  const [role, setRole] = useState("");
  const [showRegister, setShowRegister] = useState(false);

  // When this number changes, every part of the page loads its data again
  const [refresh, setRefresh] = useState(0);

  function updatePage() {
    setRefresh(refresh + 1);
  }

  function logout() {
    setToken("");
    setRole("");
  }

  // Not logged in: show the register page or the login page
  if (token === "") {
    if (showRegister) {
      return <Register apiUrl={API_URL} goToLogin={() => setShowRegister(false)} />;
    }
    return (
      <Login
        apiUrl={API_URL}
        setToken={setToken}
        setRole={setRole}
        goToRegister={() => setShowRegister(true)}
      />
    );
  }

  return (
    <div>
      <h1>Study Room Booking</h1>
      <p>
        Logged in as {role} <button onClick={logout}>Logout</button>
      </p>

      {/* Students: book rooms and manage their own bookings */}
      {role === "student" && (
        <div>
          <Rooms apiUrl={API_URL} token={token} refresh={refresh} onChange={updatePage} />
          <hr />
          <MyBooking apiUrl={API_URL} token={token} refresh={refresh} onChange={updatePage} />
        </div>
      )}

      {/* Staff: add, open and close rooms */}
      {role === "staff" && (
        <ManageRooms apiUrl={API_URL} token={token} refresh={refresh} onChange={updatePage} />
      )}
    </div>
  );
}

export default App;