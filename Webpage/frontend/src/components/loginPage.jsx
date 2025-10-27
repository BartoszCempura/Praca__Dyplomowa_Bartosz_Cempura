import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function LoginPage() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await api.post("/auth/login", { login, password });

      localStorage.setItem("access_token", response.data.access_token);
      localStorage.setItem("refresh_token", response.data.refresh_token);

      navigate("/"); // przekierowanie po zalogowaniu
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Nieprawidłowy login lub hasło");
    }
  };


  return (
    <div className="flex flex-col items-center justify-center bg-base-200 py-40">
      <form onSubmit={handleSubmit} className="card w-96 bg-base-100 shadow-xl p-6 space-y-4">
        <h2 className="text-2xl font-bold text-center">Zaloguj się</h2>

        <input type="text" placeholder="Login" className="input input-bordered w-full" value={login} onChange={(e) => setLogin(e.target.value)}/>

        <input type="password" placeholder="Hasło" className="input input-bordered w-full" value={password} onChange={(e) => setPassword(e.target.value)}/>

        <button type="submit" className="btn btn-primary w-full">Zaloguj</button>
      </form>
    </div>
  );
}
export default LoginPage;