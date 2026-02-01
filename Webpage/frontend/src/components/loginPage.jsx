import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";
import { getSessionId, clearSessionId } from "../utils/trackInteraction";

function LoginPage() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState('');
  const navigate = useNavigate();

const handleSubmit = async (e) => {
    e.preventDefault(); // submit nie przeładowuje strony
    setMessage("");

    try {

      const response = await api.post("/auth/login", { login, password }, { withCredentials: true });
      sessionStorage.setItem("access_token", response.data.access_token);
      clearSessionId(); // czyścimy poprzednie sessionID
      getSessionId(); // ustawiam sessionID po zalogowaniu
      window.dispatchEvent(new Event("loginStatusChange")); // powiadamiam navbarUserMenu o zmianie stanu logowania
      navigate("/");

      } catch (err) {
      console.error(err);
      setMessageType("error");
      setLogin("");
      setPassword("");
      e.target.reset();
      setMessage(err.response?.data?.error || "Błąd podczas logowania");

    }
  };

  return (
    <div className="flex flex-col items-center justify-center bg-base-100 py-40">
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 space-y-4 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Zaloguj się</h2>
        <form onSubmit={handleSubmit}>
          <fieldset className="fieldset">    
            <input type="text" placeholder="Login" className="input validator w-full mb-4" value={login} onChange={(e) => setLogin(e.target.value)}/>
            <input type="password" placeholder="Hasło" className="input validator w-full mb-4" value={password} onChange={(e) => setPassword(e.target.value)}/>
            <button type="submit" className="btn btn-custom w-full">Zaloguj</button>
          </fieldset>
        </form>

        {message && (
        <p className={`text-center text-sm ${messageType === 'success' ? 'text-green-600' : ''} ${messageType === 'error' ? 'text-red-600' : ''}`}>
            {message}
        </p>
          )}
     </div>
  </div>
  );
}
export default LoginPage;