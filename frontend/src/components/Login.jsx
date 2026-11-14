import { useState } from "react";

function Login({ apiUrl, setToken, setRole, goToRegister }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  // Send username and password, get back the token and the role
  function handleLogin() {
    fetch(apiUrl + "/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, password: password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.access_token) {
          setRole(data.role);
          setToken(data.access_token);
        } else {
          setMessage("Wrong username or password");
        }
      });
  }

  return (
    <div>
      <h2>Login</h2>

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

      <button onClick={handleLogin}>Login</button>
      <p>{message}</p>

      <button onClick={goToRegister}>Register</button>
    </div>
  );
}

export default Login;