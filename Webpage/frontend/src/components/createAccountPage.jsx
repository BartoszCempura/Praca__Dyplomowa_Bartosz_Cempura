import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function UserCreateAccount() {
  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [email, setEmail] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState('');
  const navigate = useNavigate();

const handleSubmit = async (e) => {
    e.preventDefault(); // submit nie przeładowuje strony
    setMessage("");


    if (password !== confirmPassword) {
      setMessage("Hasła muszą być identyczne");
      setMessageType("error");
      e.target.reset();
      return; // przerywamy wysyłanie formularza
    }

    try {

      const response = await api.post("/user_management/user", {
        login: login,
        password: password,
        email: email,
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber
      });

      setMessage(response.data.message);
      setMessageType("success");
      setLogin(""); //czyszcze pola
      setPassword("");
      setConfirmPassword("");
      setEmail("");
      setFirstName("");
      setLastName("");
      setPhoneNumber("");
      e.target.reset(); //aby nie pozostawała czerwona ramka ro zmianie hasła
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
    console.error(err);
    setMessageType("error");
    setMessage(err.response?.data?.error || "Coś poszło nie tak");
    e.target.reset();
    }
  };

  return (
    <div className="flex items-center justify-center bg-base-100 py-20">
      <div className="card w-96 bg-base-200 shadow-md shadow-black/40 p-6 border border-gray-900">
        <h2 className="text-2xl font-bold text-center">Zarejestruj konto</h2>
        <form onSubmit={handleSubmit}>
          <fieldset className="fieldset">
            <label className="label text-sm">Login:</label> 
            <input type="text" placeholder="np. Adrian123" className="input validator w-full mb-4" value={login} onChange={(e) => setLogin(e.target.value)}/>
            <label className="label text-sm">Hasło:</label>
            <input type="password" placeholder="Hasło" className="input validator w-full mb-2" minLength={8} pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" value={password} onChange={(e) => setPassword(e.target.value)}/>
            <input type="password" placeholder="Potwierdź hasło" className="input validator w-full" minLength={8} pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)}/>
            <p className="label mt-2 mb-4">Hasło: min. 8 znaków, 1 duża litera, 1 mała litera, 1 cyfra</p>
            <label className="label text-sm">Email:</label>
            <input type="email" placeholder="np. jan.kowalski@example.com" className="input validator w-full mb-4" value={email} onChange={(e) => setEmail(e.target.value)}/>
            <label className="label text-sm">Imię:</label>
            <input type="text" placeholder="Imię" className="input validator w-full mb-4" value={firstName} onChange={(e) => setFirstName(e.target.value)}/>
            <label className="label text-sm">Nazwisko:</label>
            <input type="text" placeholder="Nazwisko" className="input validator w-full mb-4" value={lastName} onChange={(e) => setLastName(e.target.value)}/>
            <label className="label text-sm">Numer telefonu:</label>
            <input type="text" placeholder="xxx xxx xxx" className="input validator w-full mb-6" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)}/>
          </fieldset>
          <button type="submit" className="btn btn-custom w-full">Zarejestruj</button>
        </form>

        {message && (
        <p className={`mt-4 text-center ${messageType === 'success' ? 'text-green-600' : ''} ${messageType === 'error' ? 'text-red-600' : ''}`}>
            {message}
        </p>
          )}
     </div>
  </div>
  );
}
export default UserCreateAccount;