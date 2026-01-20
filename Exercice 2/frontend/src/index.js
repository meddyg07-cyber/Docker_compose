import React, { useEffect, useState } from "react";
import ReactDOM from "react-dom/client";

function App() {
  const [users, setUsers] = useState([]);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [editId, setEditId] = useState(null);

  const fetchUsers = () => {
    fetch("http://localhost:3001/users")
      .then((res) => res.json())
      .then(setUsers);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const createUser = () => {
    fetch("http://localhost:3001/users", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }).then(() => {
      setUsername("");
      setPassword("");
      fetchUsers();
    });
  };

  const deleteUser = (id) => {
    fetch(`http://localhost:3001/users/${id}`, {
      method: "DELETE",
    }).then(fetchUsers);
  };

  const startEdit = (user) => {
    setEditId(user.id);
    setUsername(user.username);
    setPassword(user.password);
  };

  const updateUser = () => {
    fetch(`http://localhost:3001/users/${editId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    }).then(() => {
      setEditId(null);
      setUsername("");
      setPassword("");
      fetchUsers();
    });
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>CRUD Users</h1>

      <input
        placeholder="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        placeholder="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      {editId ? (
        <button onClick={updateUser}>Update</button>
      ) : (
        <button onClick={createUser}>Create</button>
      )}

      <hr />

      <h2>Users</h2>
      <ul>
        {users.map((u) => (
          <li key={u.id}>
            {u.id} - {u.username} - {u.password}{" "}
            <button onClick={() => startEdit(u)}>Edit</button>{" "}
            <button onClick={() => deleteUser(u.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
