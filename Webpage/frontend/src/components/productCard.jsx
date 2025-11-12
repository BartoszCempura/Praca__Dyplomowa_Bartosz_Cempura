import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api/tokenHandler";

function ProductCard({ id, name, slug, image, unit_price, price_including_promotion, variant, quantity }) {
  const [isInCart, setIsInCart] = useState(false);

  useEffect(() => {
    const checkIfInCart = async () => {
      try {
        const response = await api.get("/commerce/carts");
        const products = response.data.products || [];
        const exists = products.some((p) => p.product_id === id);
        setIsInCart(exists);
      } catch (err) {
        console.error("Błąd sprawdzania koszyka:", err);
      }
    };

    checkIfInCart();
    // nasłuch na event z innych komponentów (np. po dodaniu/usupełnieniu)
    window.addEventListener("cartChange", checkIfInCart);
    return () => window.removeEventListener("cartChange", checkIfInCart);
  }, [id]);

  const addToCart = async (change) => {
  try {  
    await api.put("/commerce/carts", { product_id: id, quantity: change });

    // 🔹 Aktualizacja localStorage
    const stored = localStorage.getItem("tempCartQuantity");
    const tempCart = stored ? JSON.parse(stored) : {};

    tempCart[id] = tempCart[id] || {};
    const currentQty = tempCart[id].quantity_user || 0;
    const newQty = currentQty + change;

    // 🔸 Zabezpieczenie: jeśli wynik byłby ujemny, pomijamy zapis
    if (change < 0 && newQty < 0) {
      console.warn(`❌ Pominięto zapis — ilość produktu ${id} byłaby ujemna.`);
      return;
    }

    tempCart[id].quantity_user = newQty;
    tempCart[id].price_including_promotion = price_including_promotion;

    localStorage.setItem("tempCartQuantity", JSON.stringify(tempCart));

    // 🔹 Odświeżamy widok koszyka
    window.dispatchEvent(new Event("cartChange"));
  } catch (err) {
    console.error(err);
    if (err.response?.status === 401) {
      alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
    } else {
      alert(err.response?.data?.error || "Coś poszło nie tak");
    }
  }
};


const [localQuantity, setLocalQuantity] = useState(() => {
  const stored = localStorage.getItem("tempCartQuantity");
  if (!stored) return 1;
  const tempCart = JSON.parse(stored);
  return tempCart[id]?.quantity_user ?? 1; // jeśli istnieje w LS — weź wartość, jeśli nie — 1
});

const updateLocalQuantity = (change) => {
  const stored = localStorage.getItem("tempCartQuantity");
  if (!stored) return;

  const tempCart = JSON.parse(stored);
  const currentProduct = tempCart[id];
  if (!currentProduct) return;

  let newQuantity = currentProduct.quantity_user + change; // mamy tutaj +1 ponieważ ze stanu jest zdejmowany 1 produkt i tym samym magazyn jest o 1 mniejszy
  if (change > 0 && newQuantity > currentProduct.quantity_db + 1) {
    alert("Brak wystarczającej ilości w magazynie");
    return;
  }

  if (newQuantity < 1) { //????
    addToCart(-1);
    delete tempCart[id];
    newQuantity = 0;
  } else {
    tempCart[id] = { ...currentProduct, quantity_user: newQuantity };
  }

  localStorage.setItem("tempCartQuantity", JSON.stringify(tempCart));
  setLocalQuantity(newQuantity); // <-- odświeża UI
  window.dispatchEvent(new Event("cartChange"));
};


  if (variant === "catalog") {
    return (
      <div className="card card-side bg-base-200 shadow-md hover:shadow-black/40 transition-shadow duration-100 w-100 grid grid-cols-2 border border-gray-900">
        <figure>
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="object-cover w-full h-full" />
          </Link>
        </figure>
        <div className="card-body flex flex-col justify-between">
          <Link to={`/product/${slug}`}>
            <h2 className="card-title">{name}</h2>
          </Link>
          
          {price_including_promotion !== unit_price ? (
            <div className="relative inline-block">
              <span className="text-md font-semibold text-success">
                ${price_including_promotion}
              </span>
              <span className="absolute right-2 -top-1 text-error line-through text-sm">
                ${unit_price}
              </span>
            </div>
          ) : (
            <span className="text-md font-semibold">
              ${price_including_promotion}
            </span>
          )}

          <div className="card-actions">
            <button
              type="button"
              onClick={() => addToCart(1)}
              className={isInCart ? "btn btn-in-cart mb-6 w-full" : "btn btn-custom mb-6 w-full"}
              disabled={isInCart} // ✅ blokada przycisku
            >
              {isInCart ? "W koszyku" : "Dodaj do koszyka"}
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (variant === "cart") {
    return (
      <div className="w-full flex items-center gap-6 bg-base-200 shadow-md border border-gray-900 rounded-lg p-4 hover:shadow-black/40 transition-shadow duration-100">
        <figure className="w-24 h-24 flex-shrink-0">
          <Link to={`/product/${slug}`}>
            <img src={image} alt={name} className="w-full h-full object-cover rounded-lg" />
          </Link>
        </figure>

        <div className="flex justify-between items-center flex-grow gap-6">
          <Link to={`/product/${slug}`} className="flex-1">
            <h2 className="text-lg font-semibold line-clamp-1">{name}</h2>
          </Link>

          <span className="font-medium whitespace-nowrap">
            ${price_including_promotion}
          </span>

          {/* Sekcja zmiany ilości */}
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-600">Ilość:</label>
            <div className="flex items-center border rounded-md overflow-hidden">
              <button
                type="button"
                className="btn btn-xs btn-ghost"
                disabled={localQuantity <= 1}
                onClick={() =>updateLocalQuantity(-1)} // zmniejsz ilość
              >
                –
              </button>
              <span className="w-10 text-center">
                {localQuantity}
                </span>
              <button
                type="button"
                className="btn btn-xs btn-ghost"
                onClick={() => updateLocalQuantity(1)} // zwiększ ilość
              >
                +
              </button>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={() => {
              // usuń z backendu
              addToCart(-quantity); ///<---- tu jest problem bo ustawiam wartośc ujemną -1 a local storrage aktualizuje na tej podstawie

              // usuń z localStorage
              const stored = localStorage.getItem("tempCartQuantity");
              if (stored) {
                const tempCart = JSON.parse(stored);
                delete tempCart[id]; // usuń produkt po id

                // jeśli koszyk pusty — usuń zmienną całkowicie
                if (Object.keys(tempCart).length === 0) {
                  localStorage.removeItem("tempCartQuantity");
                } else {
                  localStorage.setItem("tempCartQuantity", JSON.stringify(tempCart));
                }
              }

              // odśwież UI, jeśli nasłuchujesz eventu
              window.dispatchEvent(new Event("cartChange"));
            }}
            className="btn btn-sm btn-error text-white"
          >
            Usuń
          </button>
        </div>
      </div>
    );
  }

  return null;
}

export default ProductCard;
