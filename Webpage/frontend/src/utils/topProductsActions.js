import api from "../api/tokenHandler";

export async function getTopProducts() {
  try {
    const response = await api.get("/algorithms/top-products");

    return {
      topProducts: response.data.top_products || [],
      mostPurchased: response.data.most_purchased_product || null,
      purchasedThisWeek: response.data.product_purchase_history || [],
      mostViewed: response.data.top_viewed_product || null
    };

  } catch (err) {
    console.error(err);
    return {
      topProducts: [],
      mostPurchased: null,
      purchasedThisWeek: [],
      mostViewed: null
    };
  }
}
