import api from "../api/tokenHandler";

export async function getTransactions(filters = {}) {
  try {
    const response = await api.get("/commerce/transactions", {
      params: filters  // Axios automatically converts to URLSearchParams
    });

    return {
      transactions: response.data.transakcje || [],
      total: response.data.total || 0,
      page: response.data.page || 1,
      pages: response.data.pages || 1,
      hasNext: response.data.has_next || false,
      hasPrev: response.data.has_prev || false,
      nextPage: response.data.next_page || null,
      prevPage: response.data.prev_page || null
    };

  } catch (err) {
    console.error("Error fetching transactions:", err);
    throw err;
  }
}

export async function setTransactionStatus(transactionId, status) {
try {
    const payload = { status };

    const response = await api.put(
      `/commerce/admin/transactions/${transactionId}`,
      payload
    );
    return true;
} catch (err) {
    console.error(err);
    return false;
}
}