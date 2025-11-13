import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function UserProfile() {
  const [user, setUser] = useState(null);
  // zmiana hasła
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const [passwordMessage, setPasswordMessage] = useState("");
  const [passwordMessageType, setPasswordMessageType] = useState("");
  // usówanie konta
  const [deletePassword, setDeletePassword] = useState("");
  
  const [deleteMessage, setDeleteMessage] = useState("");
  const [deleteMessageType, setDeleteMessageType] = useState("");
  
  const navigate = useNavigate();

  // Pobranie danych użytkownika
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
  //------------------------------

  //Zmiana hasła
  const handleSubmitNewPassword = async (e) => {
    e.preventDefault();
    setPasswordMessage("");

    try {
      const response = await api.put("/user_management/user", {
        old_password: oldPassword,
        new_password: newPassword,
      });

  // sekcja komunikatów
      setPasswordMessage(response.data.message);

      setPasswordMessageType("success");
      setOldPassword("");
      setNewPassword("");
      e.target.reset();
    } catch (err) {  
      setPasswordMessageType("error");
      setOldPassword("");
      setNewPassword("");
      e.target.reset();

      console.error(err);
      setPasswordMessage(err.response?.data?.error || "Błąd podczas zmiany hasła");
    }
  };

  // Usuwanie konta
  const handleDeleteAccount = async (e) => {
    e.preventDefault();
    setDeleteMessage("");

    try {
      const response = await api.delete("/user_management/user", {
        data: { password: deletePassword }, // backend wymaga hasła
      });


   // sekcja komunikatów

      setDeleteMessage(response.data.message);

      setDeleteMessageType("success");
      setDeletePassword("");
      sessionStorage.removeItem("access_token");
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
      
      setDeleteMessageType("error");
      setDeletePassword("");
      console.error(err);
      setDeleteMessage(err.response?.data?.error || "Nie udało się usunąć konta");
    }
  };

  if (!user) {
    return <div className="flex justify-center py-40 text-lg">Ładowanie danych użytkownika...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center bg-base-100 py-20">

      {/* --- Sekcja danych konta --- */}
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Profil użytkownika</h2>
        <div className="space-y-2">
          <div className="flex justify-between">
            <strong>Login:</strong>
            <span>{user.login}</span>
          </div>
          <div className="flex justify-between">
            <strong>Imię i nazwisko:</strong>
            <span>{user.first_name} {user.last_name}</span>
          </div>
          <div className="flex justify-between">
            <strong>Email:</strong>
            <span>{user.email}</span>
          </div>
          <div className="flex justify-between">
            <strong>Telefon:</strong>
            <span>{user.phone_number}</span>
          </div>
        </div>
      </div>

      {/* --- Sekcja zmiany hasła --- */}
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Zmiana hasła</h2>
        <form onSubmit={handleSubmitNewPassword} className="flex flex-col items-center">
          <input type="password" placeholder="Obecne hasło" className="input validator w-full mb-4" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)}/>
          <input type="password" placeholder="Nowe hasło" className="input validator w-full mb-5" value={newPassword} onChange={(e) => setNewPassword(e.target.value)}/>
          <button type="submit" className="btn btn-custom w-full">Zmień hasło</button>

          {passwordMessage && (
            <p className={`mt-4 text-center text-sm ${passwordMessageType === "success" ? "text-green-600" : passwordMessageType === "error" ? "text-red-600" : ""}`}>
              {passwordMessage}
            </p>
          )}
        </form>
      </div>

      {/* --- Sekcja usówania konta --- */}
      <div className="card w-96 items-center bg-base-200 shadow-md shadow-black/40 p-6 mb-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center mb-6">Usuń konto</h2>
        <p className="mb-4">
          Usunięcie konta jest nieodwracalne. Wszystkie Twoje dane zostaną trwale usunięte z naszej bazy danych.
        </p>
        <button className="btn btn-custom w-full" onClick={() => document.getElementById("delete_account").showModal()}>Usuń</button>
      </div>

      {/* --- modal dla usówania konta --- */}
      <dialog id="delete_account" className="modal">
        <div className="modal-box">
          <form method="dialog">
            <button className="btn btn-sm btn-circle btn-ghost absolute right-2 top-2">✕</button>
          </form>
          <h3 className="font-bold text-lg">Potwierdzenie usunięcia konta</h3>
          <p className="py-4 mb-2">Czy na pewno chcesz usunąć swoje konto?</p>

          <form onSubmit={handleDeleteAccount}>
            <input type="password" placeholder="Podaj hasło" className="input input-bordered w-full mb-" value={deletePassword} onChange={(e) => setDeletePassword(e.target.value)} required/>
            <div className="modal-action justify-center">
              <button type="submit" className="btn btn-error text-white hover:opacity-90" style={{ width: "151px" }}>Usuń konto</button>
            </div>
          </form>

          {deleteMessage && (
            <p className={`mt-4 text-center text-sm ${deleteMessageType === "success" ? "text-green-600" : deleteMessageType === "error" ? "text-red-600" : ""}`}>
              {deleteMessage}
            </p>
          )}
        </div>
      </dialog>
    </div>
  );
}

export default UserProfile;
