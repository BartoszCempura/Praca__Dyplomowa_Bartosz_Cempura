const STORAGE_KEY = "tempCart";

export function getCart() {
  const stored = localStorage.getItem(STORAGE_KEY);
  return stored ? JSON.parse(stored) : {};
}

export function saveCart(cart) {
  if (Object.keys(cart).length === 0) {
    localStorage.removeItem(STORAGE_KEY);
  } else {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  }
  window.dispatchEvent(new Event("cartChange"));
}

export function saveCartSilent(cart) {
  if (Object.keys(cart).length === 0) {
    localStorage.removeItem(STORAGE_KEY);
  } else {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
  }
}

// ----------------------------------------
// Public API
// ----------------------------------------

export function getItem(productId) { // pobiera jednen produkt z koszyka
  const cart = getCart();
  return cart[productId] || null;
}

export function setItem(productId, data) { // ustawia/aktualizuje jeden produkt w koszyku
  const cart = getCart();
  cart[productId] = data;
  saveCart(cart);
}

export function removeItem(productId) {
  const cart = getCart();
  delete cart[productId];
  saveCart(cart);
}

export function updateQuantity(productId, change) { // pozwala na zmiane ilości produktu w koszyku - dodaje lub odejmuje
  const cart = getCart();
  const item = cart[productId];

  // jeśli produktu nie ma - nic nie rób
  if (!item) return;

  const newQuantity = item.quantity_user + change;

  // ilości <= 0 - usuń produkt
  if (newQuantity <= 0) {
    delete cart[productId];
    saveCart(cart);
    return;
  }

  // magazyn + 1 bo ze stanu zdejmujemy przy dodaniu
  if (item.quantity_db && newQuantity > item.quantity_db + 1) {
    alert("Brak wystarczającej ilości w magazynie");
    return;
  }

  cart[productId] = { // przypisuje wartośc do pola quantity_user
    ...item,
    quantity_user: newQuantity,
  };

  saveCart(cart);
}
