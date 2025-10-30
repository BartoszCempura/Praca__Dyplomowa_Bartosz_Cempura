import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/tokenHandler";

function NavbarUserMenu() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
   const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = sessionStorage.getItem("access_token");
    if (token) setIsLoggedIn(true);
  }, []);

  const handleLogin = () => navigate("/login");

  const handleLogout = async () => {
    try {
      // ✅ Wylogowanie backendowe — usunięcie refresh cookie (jeśli masz taki endpoint)
      await api.post("/auth/logout", {}, { withCredentials: true });
    } catch (err) {
      console.warn("Nie udało się wylogować po stronie backendu:", err);
    }

    // ✅ Usuwamy access token z sessionStorage
    sessionStorage.removeItem("access_token");

    setIsLoggedIn(false);
    navigate("/login");
  };

  const handleClick = async () => {
    try {
      const res = await api.get("/user_management/user"); // wywołanie endpointu chronionego @jwt_required()
      setUser(res.data);
      console.log("Dane użytkownika:", res.data);
    } catch (err) {
      console.error("Błąd pobierania danych użytkownika:", err);
      //alert(err.response?.data?.error || "Nie udało się pobrać danych użytkownika");
    }
  };

  return (
    <div className="dropdown dropdown-end">
      <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar w-14 h-14">
        <div className="w-14 rounded-full">
          <img
            alt="User avatar"
            src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
          />
        </div>
      </div>

      {isLoggedIn ? (
        <ul tabIndex={-1} className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
          <li><a onClick={handleClick} style={{ cursor: "pointer" }}>Profile</a></li>
          <li><a>Settings</a></li>
          <li><a onClick={handleLogout} className="cursor-pointer">Logout</a></li>
        </ul>
      ) : (
        <ul tabIndex={-1} className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
          <li><a>Utwórz konto</a></li>
          <li><a onClick={handleLogin} className="cursor-pointer">Zaloguj</a></li>
        </ul>
      )}
    </div>
  );
}

export default NavbarUserMenu;
