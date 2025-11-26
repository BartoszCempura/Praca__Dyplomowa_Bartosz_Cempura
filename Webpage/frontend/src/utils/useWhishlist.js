import { useState, useEffect } from "react";
import api from "../api/tokenHandler";

export function useWishlist(productId) {
  const [ inWishList, setInWishList ] = useState(false);

  async function checkIfInWishlist(productId) {
    try {
      const response = await api.get("/commerce/wishlists");
      const products = response.data || [];

      let exists = false;
        for (let i = 0; i < products.length; i++) {
          if (products[i].product.id === productId) {
            exists = true;
            break;
          }
        } 

      setInWishList(exists);
    } catch (err) {
      console.error(err);
    }
  }


  useEffect(() => {
    if (!productId) return; // hook działa TYLKO jeśli przekazano ID

    const handler = () => checkIfInWishlist(productId);

    // pierwsze sprawdzenie
    handler();

    // nasłuch na zmiany koszyka
    window.addEventListener("wishlistChange", handler);

    return () => window.removeEventListener("wishlistChange", handler);
  }, [productId]);

  return inWishList;
}