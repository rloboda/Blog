import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../services/api";  // Import axios instance

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  
  const handleRegister = async () => {
    try {
      await axios.post("/register", { username, password });
      navigate("/login");
    } catch (error) {
      alert(error.response?.data?.message || "Registration failed");
    }
  };

  return (
    <div className="flex flex-col items-center mt-20">
      <h2 className="text-2xl">Register</h2>
      <input className="border p-2 m-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input className="border p-2 m-2" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="bg-blue-500 text-white p-2 rounded" onClick={handleRegister}>Register</button>
    </div>
  );
}