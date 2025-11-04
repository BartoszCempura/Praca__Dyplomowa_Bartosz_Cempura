import api from "./axios";

api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("access_token");
    if (
      token &&
      !config.url.endsWith("/auth/refresh") &&
      !config.url.endsWith("/auth/login") &&
      !config.url.endsWith("/auth/register")
    ) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      originalRequest.url.includes("/auth/login") ||
      originalRequest.url.includes("/auth/refresh")
    ) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const res = await api.post("/auth/refresh", {}, { withCredentials: true });
        sessionStorage.setItem("access_token", res.data.access_token);
        originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        try {
          await api.post("/auth/logout", {}, { withCredentials: true });
        } catch (logoutErr) {
          console.warn("Błąd przy próbie wylogowania:", logoutErr);
        }

        sessionStorage.removeItem("access_token");
        window.dispatchEvent(new Event("loginChange"));
        setTimeout(() => {
          window.location.href = "/login";
        }, 100);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
