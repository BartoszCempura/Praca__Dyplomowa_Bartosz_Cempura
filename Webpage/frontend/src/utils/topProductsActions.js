import api from "../api/tokenHandler";

export async function getTopProducts() {
  try {
    const response = await api.get("/algorithms/top-products");

    return {
      topProducts: response.data.top_products || [],
      mostPurchased: response.data.most_purchased_product || null,
      product_purchase_history: response.data.product_purchase_history || [],
      products_purchased_this_week: response.data.products_purchased_this_week || [],
      mostViewed: response.data.top_viewed_product || null
    };

  } catch (err) {
    console.error(err);
    return {
      topProducts: [],
      mostPurchased: null,
      product_purchase_history: [],
      mostViewed: null
    };
  }
}
