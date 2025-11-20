import { useState, useEffect } from "react";
import api, { isAuthenticated } from "../api/tokenHandler";
import { getCart, getItem, setItem, updateQuantity, removeItem, clearCart as clearLocalCart } from "./tempCartStorage";

export function useCart(productId = null) {
  const [isInCart, setIsInCart] = useState(false);

  // Funkcja dodawania produktu do koszyka. ardument "product" to obiekt zawierający id, quantity, price_including_promotion
  // change to zmiana ilości (dodatnia lub ujemna)

  async function addToCart(product, change) {

    if (!isAuthenticated()) {
      alert("Musisz być zalogowany, aby dodać produkt do koszyka!");
      window.location.href = "/login";
      return;
    }

    try {
      await api.put("/commerce/carts", {product_id: product.id, quantity: change,});

      const existing = getItem(product.id);

      if (!existing) {
        setItem(product.id, {
          quantity_user: 1,
          quantity_db: product.quantity,
          price_including_promotion: product.price_including_promotion,
        });
      } else {
        updateQuantity(product.id, change);
      }

      setIsInCart(true);
    } catch (err) {
      console.error(err);
      if (err.response?.status === 401) {
        alert("Sesja wygasła. Zaloguj się ponownie.");
      } else {
        alert(err.response?.data?.error || "Coś poszło nie tak");
      }
    }
  }

  // funkcja pozwalająca na usunięcie produktu z koszyka
  // usówana jest ilośc z koszyka w bazie oraz z local storage
  // domyślnie program jesttak napisany że usówa tylko 1 sztuke produktu

  async function removeFromCart(id, quantity) {
    try {
      await api.put("/commerce/carts", {
        product_id: id,
        quantity: -quantity,
      });

      removeItem(id);

    } catch (err) {
      console.error("Błąd usuwania z koszyka:", err);
    }
  }

  // funkcja sprawdzająca czy produkt znajduje się w koszyku
  // pozwala ustawić wartość isInCart a za jej pomocą operować przyciskiem dodania do koszyka

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

   async function clearCart() {
    const cart = getCart();
    const productIds = Object.keys(cart);

    try {
      // Usuń każdy produkt z bazy danych
      const promises = productIds.map((id) => {
        return api.put("/commerce/carts", {
          product_id: parseInt(id),
          quantity: -1,
        });
      });

      await Promise.all(promises);

       clearLocalCart();
      setIsInCart(false);

    } catch (err) {
      console.error("Błąd czyszczenia koszyka:", err);
      alert("Nie udało się wyczyścić koszyka");
    }
  }

  // efekt uruchamiany przy zmianie productId (id produktu)
  // pozwala na automatyczną weryfikacje obecności produktu w koszyku

   useEffect(() => {
    if (!productId) return; // hook działa TYLKO jeśli przekazano ID

    const handler = () => checkIfInCart(productId);

    // pierwsze sprawdzenie
    handler();

    // nasłuch na zmiany koszyka
    window.addEventListener("cartChange", handler);

    return () => window.removeEventListener("cartChange", handler);
  }, [productId]);

  // exportujemy wszystkie funkcje i zmienną do bezpośredniego użycia w komponencie
  return { isInCart, setIsInCart, addToCart, removeFromCart, checkIfInCart, clearCart };
}