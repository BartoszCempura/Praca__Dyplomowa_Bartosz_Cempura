import { useState, useEffect } from "react";
import api from "../api/tokenHandler";

// Współdzielony stan poza komponentem - jeden dla całej aplikacji
let cachedIds = new Set();
let listeners = new Set();

async function fetchWishlist() {
  try {
    const response = await api.get("/commerce/wishlists");
    const products = response.data || [];
    cachedIds = new Set(products.map(p => p.id));
    // Powiadom wszystkie komponenty które używają hooka
    listeners.forEach(fn=> fn(cachedIds));
  }catch (err) {
    console.error(err);
  }
}

window.addEventListener("WhishlistChange", fetchWishlist);
window.addEventListener("loginStatusChange", fetchWishlist);

export function useWishlist(productId = null) {
 const [ids, setIds] = useState(cachedIds);

  useEffect(() => {
    const update = (newIds) => setIds(new Set(newIds));
    listeners.add(update);

    // Pierwsze załadowanie — pobierz tylko jeśli cache pusty
    if (cachedIds.size === 0 && sessionStorage.getItem("access_token")) {
      fetchWishlist();
    }

    return () => listeners.delete(update);
  }, []);

  if (productId === null) return ids.size > 0;
  return ids.has(productId);
}