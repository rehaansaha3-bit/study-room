import { useState } from "react";

function Register({ apiUrl, goToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("student");
  const [message, setMessage] = useState("");

  // Create a new user, then go back to the login page
  function handleRegister() {
    fetch(apiUrl + "/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_name: username, password: password, role: role }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.detail) {
          setMessage(data.detail);
        } else {
          goToLogin();
        }
      });
  }

  return (
    <div>
      <h2>Register</h2>

      <input
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <br />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <br />
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="student">Student</option>
        <option value="staff">Staff</option>
      </select>
      <br />

      <button onClick={handleRegister}>Register</button>
      <p>{message}</p>

      <button onClick={goToLogin}>Back to login</button>
    </div>
  );
}

export default Register;