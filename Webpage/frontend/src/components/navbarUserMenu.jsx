import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";
import { useCart } from "../utils/realCart";

function NavbarUserMenu() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
  const navigate = useNavigate();
  const { clearCart } = useCart();

useEffect(() => {
  const handleLoginStatusChange = async () => {
    const token = sessionStorage.getItem("access_token");

    if (token) {
      setIsLoggedIn(true)

      try {
        const response = await api.get("/user_management/user");
        setUser(response.data);
      } catch (err) {
        console.error(err);
      }
    } else {
      setIsLoggedIn(false)
    }
  };

  handleLoginStatusChange(); // pobranie początkowego stanu
  window.addEventListener("loginStatusChange", handleLoginStatusChange);
  return () => window.removeEventListener("loginStatusChange", handleLoginStatusChange); //sprzątanie
}, []);
 
  const handleLogin = () => navigate("/login");
  const handleRegister = () => navigate("/register");
  const handleAdmin = () => navigate("/admin");


  const handleLogout = async () => {

      clearCart(); // czyścimy koszyk w local storage 

    try {   
      await api.post("/auth/logout", {}, { withCredentials: true });
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.error || "Something went wrong");
    }
    sessionStorage.removeItem("access_token");
    window.dispatchEvent(new Event("loginStatusChange"));
    setIsLoggedIn(false);
    navigate("/login");
  };


const handleProfile = () => navigate("/user");

  return (
    <div className="dropdown dropdown-end">
      <div className="indicator">
        <div className="indicator-item indicator-top indicator-end">
          {isLoggedIn ? (
            <div aria-label="success" className="status status-success status-lg"></div>
          ) : (
            <div aria-label="warning" className="status status-neutral status-lg"></div>
          )}
        </div>

        <div tabIndex={0} role="button" className="group btn btn-ghost btn-circle avatar w-14 h-14 shadow-sm hover:shadow-amber-500 transition-shadow duration-100">
          <div className="w-14 rounded-full">
            <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-8 w-8 mx-auto mt-2.5 stroke-cyan-500 transition-colors duration-200 group-hover:stroke-amber-500"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <circle cx="12" cy="7" r="4" />
                <path d="M5.5 21a8.38 8.38 0 0113 0" />
              </svg>
          </div>
        </div>
      </div>
      {/*Menu*/}
      {isLoggedIn ? (
        <ul tabIndex={-1} className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
          <li><a onClick={handleProfile} style={{ cursor: "pointer" }}>Profil użytkownika</a></li>
          {user?.role === "admin" && (
            <li><a onClick={handleAdmin}>Kokpit</a></li>
          )}
          <li><a>Ustawienia (brak implementacji)</a></li>
          <li><a onClick={handleLogout} className="cursor-pointer">Wyloguj</a></li>
        </ul>
      ) : (
        <ul tabIndex={-1} className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
          <li><a onClick={handleRegister} className="cursor-pointer">Utwórz konto</a></li>
          <li><a onClick={handleLogin} className="cursor-pointer">Zaloguj</a></li>
        </ul>
      )}
    </div>
  );
}

export default NavbarUserMenu;
