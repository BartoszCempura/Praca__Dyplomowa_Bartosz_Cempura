import api from "../api/tokenHandler";

export async function getProductsInPromotion(promotionId) {
    const response = await api.get(`/catalog/product-promotions/${promotionId}`);
    return response.data;
}
