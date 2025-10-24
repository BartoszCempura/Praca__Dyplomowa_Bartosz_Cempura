import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function NavbarUserMenu() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) setIsLoggedIn(true);
  }, []);

  const handleLogin = () => navigate("/login");

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    setIsLoggedIn(false);
    navigate("/login");
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
          <li><a>Profile</a></li>
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
