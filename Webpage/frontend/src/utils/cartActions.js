import { useState, useEffect } from "react";
import api, { isAuthenticated } from "../api/tokenHandler";
import { getCart, getItem, setItem, updateQuantity, removeItem, clearCart as clearLocalCart } from "./tempCartStorage";


  // Funkcja dodawania produktu do koszyka. ardument "product" to obiekt zawierający id, quantity, price_including_promotion
  // change to zmiana ilości (dodatnia lub ujemna)

export async function addToCart(product, change) {

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

export async function removeFromCart(id, quantity) {
  try {
    await api.put("/commerce/carts", {product_id: id, quantity: -quantity,});

    removeItem(id);

  } catch (err) {
    console.error(err);
  }
}

// funkcja pozwalająca na usunięcie wszystkich produktów z koszyka i usunięcie pliku local storage

export async function clearCart() {
  const cart = getCart();
  const productIds = Object.keys(cart);

  try {
      // Usuń każdy produkt obecny w koszyku
    const promises = productIds.map((id) => {
      return api.put("/commerce/carts", {product_id: parseInt(id),quantity: -1,});
    });

    await Promise.all(promises);

    clearLocalCart();

  } catch (err) {
    console.error(err);
  }
}


