import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavbarUserMenu from "./navbarUserMenu";
import { getCart } from "../utils/tempCartStorage";
import { refreshTempCart } from "../utils/cartActions";

function Navbar() {
  const [query, setQuery] = useState("");
  const [cartItems, setCartItems] = useState(0);
  const [cartValue, setCartValue] = useState(0);
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?search=${encodeURIComponent(query.trim())}`);
    }
  };

  useEffect(() => {
    const fetchCart = async () => {
      try {

        const cart = getCart();
        const values = Object.values(cart);

        const totalItems = values.reduce((sum, item) => sum + (item.quantity_user || 0), 0);
        const totalValue = values.reduce((sum, item) => {
          return sum + (item.quantity_user || 0) * parseFloat(item.price_including_promotion || 0);
        }, 0);

        setCartItems(totalItems);
        setCartValue(totalValue);

      } catch (err) {
        if (err.response?.status === 401) {
          // sesja wygasła — brak koszyka
          setCartItems(0);
          setCartValue(0);
        } else {
          console.error(err);
        }
      }
    };

    // jeśli użytkownik jest zalogowany pobierane są dane o koszyku - od razu po załadowaniu navbar
    if (sessionStorage.getItem("access_token")) {
      fetchCart();
    }

    // jak zostanie wyemitowany loginChange to zachodzą zmianyw elemencie
    const handleLoginStatusChange = async () => {
      if (sessionStorage.getItem("access_token")) {
        const { totalItems, totalValue } = await refreshTempCart();
        setCartItems(totalItems);
        setCartValue(totalValue);
      } else {
        setCartItems(0);
        setCartValue(0);
      }
    };
    // jak zostanie zaktualizowany koszyk zachodzą zmiany w elemencie
    const handleCartChange = () => fetchCart();

    window.addEventListener("loginStatusChange", handleLoginStatusChange);
    window.addEventListener("cartChange", handleCartChange);

    return () => {
      window.removeEventListener("loginStatusChange", handleLoginStatusChange);
      window.removeEventListener("cartChange", handleCartChange);
    };
  }, []);

  return (
    <div className="navbar bg-base-200 grid grid-cols-3 items-center px-8 py-4 shadow-md z-50 relative">
      <div className="flex justify-start">
        <div className="flex items-center">
          <a href="/">
            <img src="/LOGO.svg" className="h-20 mr-2" alt="TechTown Logo" />
          </a>
          <a href="/" className="ml-3 hidden sm:inline-flex group">
            <div className="flex flex-col font-bold text-2xl relative">
              <p className="inline-block relative">
                TechTown
                <span className="absolute -bottom-1 left-0 w-0 group-hover:w-[120%] h-[2px] bg-gradient-to-r from-cyan-500 via-cyan-200 to-amber-600 transition-all duration-300"></span>
              </p>
            </div>
          </a>
        </div>
      </div>

      <div className="flex justify-center">
        <form onSubmit={handleSearch}>
          <input type="text" placeholder="Szukaj produktu..." className="input input-bordered w-24 md:w-80" value={query} onChange={(e) => setQuery(e.target.value)}/>
        </form>
      </div>

      <div className="justify-end flex gap-8">

        <div tabIndex={0} role="button" className="group btn btn-ghost btn-circle avatar w-14 h-14 shadow-sm hover:shadow-amber-500 transition-shadow duration-100" onClick={() => navigate("/cart")}>
          <div className="w-14 rounded-full">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              className="h-8 w-8 mx-auto mt-2.5 transition-colors duration-200 group-hover:stroke-amber-500" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
              />
            </svg>
          </div>
        </div>

        {/* CART DROPDOWN */}
        <div className="dropdown dropdown-end">
          <div tabIndex={0} role="button" className="group btn btn-ghost btn-circle w-14 h-14 shadow-sm hover:shadow-amber-500 transition-shadow duration-100">
            <div className="indicator">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 transition-colors duration-200 group-hover:stroke-amber-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0
                  0a2 2 0 100 4 2 2 0 000-4zm-8
                  2a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              <span className="badge badge-sm indicator-item">{cartItems}</span>
            </div>
          </div>
          <div tabIndex={0} className="card card-compact dropdown-content bg-base-100 z-1 mt-3 w-52 shadow">
            <div className="card-body">
              <span className="text-lg font-bold"> Przedmioty: {cartItems}</span>
              <span className="text-info mb-2">
                Wartość: {cartValue.toFixed(2)} zł
              </span>
              <div className="card-actions" onClick={() => navigate("/cart")}>
                <button className="btn btn-custom btn-block">Zobacz koszyk</button>
              </div>
            </div>
          </div>
        </div>

        <NavbarUserMenu />
      </div>
    </div>
  );
}

export default Navbar;
