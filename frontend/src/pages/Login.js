import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../services/api";  // Import axios instance

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post("/login", { username, password });
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (error) {
      alert(error.response?.data?.message || "Login failed");
    }
  };

  return (
    <div className="flex flex-col items-center mt-20">
      <h2 className="text-2xl">Login</h2>
      <input className="border p-2 m-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input className="border p-2 m-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="bg-green-500 text-white p-2 rounded" onClick={handleLogin}>Login</button>
    </div>
  );
}
