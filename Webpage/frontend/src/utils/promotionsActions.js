import api from "../api/tokenHandler";

export async function getProductsInPromotion(promotionId) {
  try {
    const response = await api.get(`/catalog/product-promotions/${promotionId}`);

    return response.data || [];

  } catch (err) {
    console.error(err);
    return [];
  }
}
