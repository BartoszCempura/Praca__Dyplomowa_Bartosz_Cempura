import api, { isAuthenticated } from "../api/tokenHandler";
import { getCart, getItem, setItem, updateQuantity, removeItem, saveCart, clearCart as clearLocalCart } from "./tempCartStorage";

  // Funkcja dodawania produktu do koszyka. ardument "product" to obiekt zawierający id, quantity, unit_price_with_discount
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
        unit_price_with_discount: product.unit_price_with_discount,
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

// funkcja zastosowana w przypadku gdy użytkownika wylogowało z sesji - odświeża koszyk w local storage na podstawie danych z backendu po ponownym zalogowaniu

export async function refreshTempCart() {
  try {
    const response = await api.get("/commerce/carts");
    const cartProducts = response.data.products || [];

    if (cartProducts.length === 0) {
      saveCart({});
      return { totalItems: 0, totalValue: 0 };
    }

    const tempCart = getCart();

    const productIds = cartProducts.map(p => p.product_id).join(",");
    const responseProducts = await api.get(`/catalog/products?product_ids=${productIds}`);
    const productsData = responseProducts.data.products;

    productsData.forEach(productData => {
      const prev = tempCart[productData.id] || {};
      tempCart[productData.id] = {
        quantity_db: productData.quantity,
        quantity_user: prev.quantity_user || 1,
        unit_price_with_discount: productData.unit_price_with_discount,
      };
    });

    saveCart(tempCart);

    const values = Object.values(tempCart);

    const totalItems = values.reduce((s, p) => s + (p.quantity_user || 0), 0);
    const totalValue = values.reduce((s, p) => s + p.quantity_user * parseFloat(p.unit_price_with_discount), 0);

    return { totalItems, totalValue };

  } catch (err) {
    console.error("Błąd podczas odświeżania koszyka:", err);
    return { totalItems: 0, totalValue: 0 };
  }
}

export async function getDeliveryMethods() {
 try {
    const response = await api.get("/commerce/delivery-methods");
    return response.data || [];
  } catch (err) {
    console.error(err);
    return [];
  }
}

export async function getPaymentMethods() {
  try {
    const response = await api.get("/commerce/payment-methods");
    return response.data || [];
  } catch (err) {
    console.error(err);
    return [];
  }
}

export async function getUserAdresses() {
  try {
    const response = await api.get("user_management/addresses");
    return response.data || [];
  } catch (err) {
    console.error(err);
    return [];
  }
}

export async function mergeCartAndLocal() {
  try {
    const response = await api.get("/commerce/carts");
    const backendData = response.data?.products || [];

    const mergedData = backendData.map(p => {
      const localItem = getItem(p.product_id);

      return {
        ...p,
        quantity: localItem?.quantity_user ?? p.quantity
      };
    });

    return mergedData;
  } catch (err) {
    console.error("mergeCartAndLocal error:", err);
    return []; 
  }
}

export async function closePurchase(payLoad) {
  try {
    const response = await api.post("/commerce/transactions", payLoad);
    const successMessage = response.data?.message || "Transakcja zakończona pomyślnie";
    alert(successMessage);
    return { success: true};
  } catch (err) {
    console.error(err);
    const errorMessage = err.response.data?.error || "Wystąpił błąd podczas finalizacji transakcji!";
    alert(errorMessage);
    return { success: false};
  }

}