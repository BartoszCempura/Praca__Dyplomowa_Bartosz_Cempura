import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import NavbarUserMenu from "./navbarUserMenu";
import api from "../api/tokenHandler";

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
        const response = await api.get("/commerce/carts");
        const data = response.data;

        if (data.products) {
          let totalItems = 0; // liczymy ilość przedmiotów w koszyku poprzez sume quantity z CartProducts

          for (let i = 0; i < data.products.length; i++) {
            const product = data.products[i];
            totalItems += product.quantity || 0;
          }

          setCartItems(totalItems);
          setCartValue(parseFloat(data.total_products_cost) || 0); // total_products_cost jest konwertowany na string w endpoincie, więc parsujemy na float
        } else {
          // jak pusty koszyk to mamy wartość 0
          setCartItems(0);
          setCartValue(0);
        }
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
    const handleLoginStatusChange = () => {
      if (sessionStorage.getItem("access_token")) {
        fetchCart();
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
          <img src="/LOGO.svg" className="h-20 mr-2" alt="TechTown Logo" />
          <a href="/" className="btn btn-ghost text-xl hidden sm:inline-flex">
            TechTown
          </a>
        </div>
      </div>

      <div className="flex justify-center">
        <form onSubmit={handleSearch}>
          <input type="text" placeholder="Szukaj produktu..." className="input input-bordered w-24 md:w-80" value={query} onChange={(e) => setQuery(e.target.value)}/>
        </form>
      </div>

      <div className="justify-end flex gap-8">
        {/* CART DROPDOWN */}
        <div className="dropdown dropdown-end">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle w-14 h-14">
            <div className="indicator">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
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
