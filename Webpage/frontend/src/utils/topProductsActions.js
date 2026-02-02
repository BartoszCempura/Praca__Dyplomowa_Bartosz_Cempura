import api from "../api/tokenHandler";

export async function getTopProducts() {
  try {
    const response = await api.get("/algorithms/top-products");

    return response.data || [];

  } catch (err) {
    console.error(err);
    return [];
  }
}
