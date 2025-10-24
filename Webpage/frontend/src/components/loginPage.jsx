import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [login, setLogin] = useState("");     // <-- tu zmiana
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:5000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        login,          // <-- zamiast email
        password,
      }),
    });

    const data = await res.json();

    if (res.ok) {
      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);
      localStorage.setItem("user", JSON.stringify(data.user));
      navigate("/");
    } else {
      alert(data.error || "Nieprawidłowy login lub hasło");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-base-200">
      <form
        onSubmit={handleSubmit}
        className="card w-96 bg-base-100 shadow-xl p-6 space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Zaloguj się</h2>

        <input
          type="text"
          placeholder="Login"
          className="input input-bordered w-full"
          value={login}
          onChange={(e) => setLogin(e.target.value)}
        />

        <input
          type="password"
          placeholder="Hasło"
          className="input input-bordered w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit" className="btn btn-primary w-full">
          Zaloguj
        </button>
      </form>
    </div>
  );
}
export default LoginPage;