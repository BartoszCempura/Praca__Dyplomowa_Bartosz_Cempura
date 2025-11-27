import { useState, useEffect } from "react";
import api from "../api/tokenHandler";

export function useWishlist(productId = null) {
  const [ inWishList, setInWishList ] = useState(false);

  async function checkIfInWishlist() {
    try {
      const response = await api.get("/commerce/wishlists");
      const products = response.data || [];

      if (!productId) {
        setInWishList(products.length > 0);
        return;
      }

      let exists = false;
        for (let i = 0; i < products.length; i++) {
          if (products[i].id === productId) {
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
    
    checkIfInWishlist();

    const handler = () => checkIfInWishlist();

    // nasłuch na zmiany koszyka
    window.addEventListener("wishlistChange", handler);

    return () => window.removeEventListener("wishlistChange", handler);
  }, [productId]);

  return inWishList;
}