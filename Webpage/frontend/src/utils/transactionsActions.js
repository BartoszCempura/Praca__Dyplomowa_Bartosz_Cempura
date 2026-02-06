import api from "../api/tokenHandler";

export async function getTransactions(filters = {}) {
  try {
    const response = await api.get("/commerce/transactions", {
      params: filters
    });

    const { transakcje, pagination } = response.data;

    return {
      transactions: transakcje || [],
      total: pagination?.total || 0,
      page: pagination?.page || 1,
      pages: pagination?.pages || 1,
      hasNext: pagination?.has_next || false,
      hasPrev: pagination?.has_prev || false,
      nextPage: pagination?.next_page || null,
      prevPage: pagination?.prev_page || null
    };

  } catch (err) {
    console.error("Error fetching transactions:", err);
    throw err;
  }
}

export async function setTransactionStatus(transactionId, status) {
try {
     await api.put(
      `/commerce/admin/transactions/${transactionId}`,
      { status }
    );
    return true;
} catch (err) {
    console.error(err);
    return false;
}
}