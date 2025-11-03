import { useEffect, useState } from "react";
import api from "../api/tokenHandler";

function UserProfile() {
  const [user, setUser] = useState(null);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState('');

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const response = await api.get("/user_management/user");
        setUser(response.data);
      } catch (err) {
        console.error(err);
        alert(err.response?.data?.error || "Błąd podczas pobierania danych użytkownika");
      }
    };

    fetchUserData();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");

    try {
  const response = await api.put("/user_management/user", {
    old_password: oldPassword,
    new_password: newPassword,
  });

    setMessage(response.data.message);
    setMessageType("success");
    setOldPassword(""); //czyszcze pola
    setNewPassword("");
    e.target.reset(); //aby nie pozostawała czerwona ramka ro zmianie hasła
    } catch (err) {
    console.error(err);
    setMessageType("error");
    setOldPassword("");
    setNewPassword("");
    e.target.reset();
    setMessage(err.response?.data?.error || "Błąd podczas zmiany hasła");

    }
  };

  if (!user) {
    return <div className="flex justify-center py-40 text-lg">Ładowanie danych użytkownika...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center bg-base-100 py-20">
      {/* Sekcja profilu */}
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 space-y-4 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Profil użytkownika</h2>
        <div className="space-y-2">
            <div className="flex justify-between">
                <strong>Login:</strong> 
                <span>{user.login}</span>
            </div>
        </div>
        <div className="space-y-2">
            <div className="flex justify-between">
                <strong>Imię i nazwisko:</strong> 
                <span>{user.first_name} {user.last_name}</span>
            </div>
        </div>
        <div className="space-y-2">
            <div className="flex justify-between">
                <strong>Email:</strong> 
                <span>{user.email}</span>
            </div>
        </div>
        <div className="space-y-2">
            <div className="flex justify-between">
                <strong>Numer telefonu:</strong> 
                <span>{user.phone_number}</span>
            </div>
        </div>
      </div>

      {/* Sekcja zmiany hasła */}
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 space-y-4 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Zmiana hasła</h2>
        <form onSubmit={handleSubmit} className="flex flex-col">
            <input type="password" placeholder="Obecne hasło" className="input validator w-full mb-4" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} required />
            <input type="password" placeholder="Nowe hasło" className="input validator w-full mb-4" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
            <button type="submit" className="btn btn-custom w-full">Zmień hasło</button>
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

export default UserProfile;

/*
minLength={8}
            pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
            */