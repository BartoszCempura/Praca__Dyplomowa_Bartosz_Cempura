import { useState, useEffect } from "react";
import api from "../api/tokenHandler";


export function useCart(productId) {
  const [isInCart, setIsInCart] = useState(false);

  async function checkIfInCart(productId) {
    try {
      const response = await api.get("/commerce/carts");
      const products = response.data.products || [];

      let exists = false; // sprawdzamy czy produkt znajduje się juz w koszyku - wymagane dla mechanizmu wyłączania przycisku Dodaj do koszyka
        for (let i = 0; i < products.length; i++) {
          if (products[i].product_id === productId) {
            exists = true;
            break;
          }
        } 

      setIsInCart(exists);
    } catch (err) {
      console.error(err);
    }
  }


  useEffect(() => {
    if (!productId) return; // hook działa TYLKO jeśli przekazano ID

    const handler = () => checkIfInCart(productId);

    // pierwsze sprawdzenie
    handler();

    // nasłuch na zmiany koszyka
    window.addEventListener("cartChange", handler);

    return () => window.removeEventListener("cartChange", handler);
  }, [productId]);

  return isInCart;
}