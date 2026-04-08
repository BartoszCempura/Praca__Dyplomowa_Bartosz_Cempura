import api from "../api/tokenHandler";

const CACHE_DURATION = 60 * 60 * 1000; // 1 godzina w ms

let cache = {
  data: null,
  timestamp: null
};

async function fetchAndUpdateCache() {
    const response = await api.get("/algorithms/top-products");
    cache.data = {
      topProducts: response.data.top_products || [],
      mostPurchased: response.data.most_purchased_product || null,
      product_purchase_history: response.data.product_purchase_history || [],
      products_purchased_this_week: response.data.products_purchased_this_week || [],
      mostViewed: response.data.top_viewed_product || null
    };
    cache.timestamp = Date.now();
    return cache.data;
}

export function invalidateCache() {
  cache.data = null;
  cache.timestamp = null;
}

window.addEventListener("loginStatusChange", invalidateCache);
// Uruchamia się automatycznie co godzinę gdy moduł jest załadowany
setInterval(fetchAndUpdateCache, CACHE_DURATION);

export async function getTopProducts() {

  const isCacheValid = cache.data && cache.timestamp &&
    (Date.now() - cache.timestamp < CACHE_DURATION);

  if (isCacheValid) {
    return cache.data;
  }

  // Cache pusty (pierwsze uruchomienie) — pobierz od razu
  return await fetchAndUpdateCache();

}