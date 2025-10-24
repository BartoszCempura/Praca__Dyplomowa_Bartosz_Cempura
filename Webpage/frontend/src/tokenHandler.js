export async function apiFetch(url, options = {}) {
  const token = localStorage.getItem("access_token");

  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options.headers,
    },
  });

  // jeśli access_token wygasł, spróbuj odświeżyć
  if (res.status === 401 && localStorage.getItem("refresh_token")) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      return apiFetch(url, options); // spróbuj ponownie
    }
  }

  return res;
}

async function refreshAccessToken() {
  const refreshToken = localStorage.getItem("refresh_token");
  if (!refreshToken) return false;

  const res = await fetch("http://localhost:5000/auth/refresh", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${refreshToken}`,
    },
  });

  if (res.ok) {
    const data = await res.json();
    localStorage.setItem("access_token", data.access_token);
    return true;
  }

  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  localStorage.removeItem("user");
  return false;
}
