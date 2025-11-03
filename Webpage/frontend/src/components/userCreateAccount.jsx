import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function UserCreateAccount() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState('');
  const navigate = useNavigate();

const handleSubmit = async (e) => {
    e.preventDefault(); // submit nie przeładowuje strony
    setMessage("");

    try {

      const response = await api.get("/user_management/user");


    setMessage(response.data.message);
    setMessageType("success");
    setLogin(""); //czyszcze pola
    setPassword("");
    e.target.reset(); //aby nie pozostawała czerwona ramka ro zmianie hasła
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
        <form onSubmit={handleSubmit} className="cflex flex-col">    
          <input type="text" placeholder="Login" className="input validator w-full mb-4" value={login} onChange={(e) => setLogin(e.target.value)}/>
          <input type="password" placeholder="Hasło" className="input validator w-full mb-4" value={password} onChange={(e) => setPassword(e.target.value)}/>
          <button type="submit" className="btn btn-custom w-full">Zaloguj</button>
        </form>

        {message && (
        <p className={` ${messageType === 'success' ? 'text-green-600' : ''} ${messageType === 'error' ? 'text-red-600' : ''}`}>
            {message}
        </p>
          )}
     </div>
  </div>
  );
}
export default UserCreateAccount;