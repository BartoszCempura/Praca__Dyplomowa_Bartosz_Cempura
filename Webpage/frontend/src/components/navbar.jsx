import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Navbar() {
  const [query, setQuery] = useState("");
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim()) {
      navigate(`/search?search=${encodeURIComponent(query.trim())}`);
    }
  };
  return (
    <div className="navbar bg-base-200 grid grid-cols-3 items-center px-8 py-4 shadow-md z-50 relative">
      <div className="flex justify-start">
        <div className="flex items-center">
            <img src="/LOGO.svg" className="h-20 mr-2" alt="TechTown Logo" />
            <a href="http://localhost:5173/" className="btn btn-ghost text-xl hidden sm:inline-flex">TechTown</a>
        </div>
      </div>

      <div className="flex justify-center">
        <form onSubmit={handleSearch}>
          <input
            type="text"
            placeholder="Szukaj produktu..."
            className="input input-bordered w-24 md:w-80"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </form>
      </div>

      <div className="justify-end flex gap-8">
        {/* CART DROPDOWN */}
        <div className="dropdown dropdown-end">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle w-14 h-14">
            <div className="indicator">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2"
                  d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0
                  0a2 2 0 100 4 2 2 0 000-4zm-8
                  2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              <span className="badge badge-sm indicator-item">8</span>
            </div>
          </div>
          <div tabIndex={0} className="card card-compact dropdown-content bg-base-100 z-1 mt-3 w-52 shadow">
            <div className="card-body">
              <span className="text-lg font-bold">8 Items</span>
              <span className="text-info">Subtotal: $999</span>
              <div className="card-actions">
                <button className="btn btn-primary btn-block">View cart</button>
              </div>
            </div>
          </div>
        </div>

        {/* USER DROPDOWN */}
        <div className="dropdown dropdown-end">
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle avatar w-14 h-14">
            <div className="w-14 rounded-full">
              <img
                alt="User avatar"
                src="https://img.daisyui.com/images/stock/photo-1534528741775-53994a69daeb.webp"
              />
            </div>
          </div>
          <ul tabIndex={-1} className="menu menu-sm dropdown-content bg-base-100 rounded-box z-1 mt-3 w-52 p-2 shadow">
            <li><a>Profile</a></li>
            <li><a>Settings</a></li>
            <li><a>Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default Navbar;
