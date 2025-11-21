import api from "./axios";
import { clearCart } from "../utils/tempCartStorage";

// lista publicznych endpointów
const PUBLIC_ENDPOINTS = [
  "/auth/refresh",
  "/auth/login",
  "/auth/register"
];

// Helper do sprawdzania czy endpoint jest publiczny
function isPublicEndpoint(url) {
  return PUBLIC_ENDPOINTS.some(endpoint => url.endsWith(endpoint));
}

//Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("access_token");
    
    if (token && !isPublicEndpoint(config.url)) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Dla publicznych endpointów nie próbuj odświeżać tokena
    if (isPublicEndpoint(originalRequest.url)) {
      return Promise.reject(error);
    }

    // Dla pozostałych - standard refresh flow
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
        clearCart();
        sessionStorage.removeItem("access_token");
        window.dispatchEvent(new Event("loginStatusChange"));
        setTimeout(() => {
          window.location.href = "/login";
        }, 100);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

//helper do sprawdzania autentykacji
export function isAuthenticated() {
  return !!sessionStorage.getItem("access_token");
}

export default api;