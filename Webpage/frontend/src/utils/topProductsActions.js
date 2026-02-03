import api from "../api/tokenHandler";

export async function getTopProducts() {
  try {
    const response = await api.get("/algorithms/top-products");

    return {
      topProducts: response.data.top_products || [],
      mostPurchased: response.data.most_purchased_product || null
    };

  } catch (err) {
    console.error(err);
    return [];
  }
}
