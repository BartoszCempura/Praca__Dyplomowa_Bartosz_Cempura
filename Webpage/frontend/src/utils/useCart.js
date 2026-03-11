import { useState, useEffect } from "react";
import { getItem } from "../utils/tempCartStorage";

export function useCart(productId) {
  const [isInCart, setIsInCart] = useState(false);

  useEffect(() => {
    if (!productId) return;

    const check = () => {
      const item = getItem(productId);
      setIsInCart(!!item);
    };

    const handler = (e) => {
      if (!e.detail) return;

      if (e.detail.productId === productId) {
        check();
      }
    };

    check(); // pierwsze sprawdzenie

    window.addEventListener("cartChange", handler);
    return () => window.removeEventListener("cartChange", handler);

  }, [productId]);

  return isInCart;
}