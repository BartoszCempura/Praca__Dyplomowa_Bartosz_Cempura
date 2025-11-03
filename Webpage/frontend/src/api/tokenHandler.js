import api from "./axios";

// request interceptor — dodaje access token z sessionStorage
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem("access_token");
    // NIE dodawaj Authorization dla /auth/refresh (ani /login itd.)
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
// response interceptor — obsługuje odnowienie tokenu, jeśli access token wygasł
api.interceptors.response.use(
  (response) => response,  // po prostu zwraca response, jeśli jest OK
  async (error) => {        // to jest funkcja wywoływana przy błędzie
    const originalRequest = error.config; // zachowujemy info o pierwotnym requestcie

    if (
      originalRequest.url.includes("/auth/login") ||
      originalRequest.url.includes("/auth/refresh") ||
      originalRequest.url.includes("/user_management/user")
    ) {
      return Promise.reject(error);
    }

    // jeśli status 401 (Unauthorized) i nie próbowaliśmy jeszcze odświeżyć tokenu
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const res = await api.post("/auth/refresh", {}, { withCredentials: true });
        sessionStorage.setItem("access_token", res.data.access_token);

        // ustawiamy nowy access token w headers oryginalnego requestu
        originalRequest.headers.Authorization = `Bearer ${res.data.access_token}`;

        // powtarzamy pierwotne żądanie z nowym tokenem
        return api(originalRequest);
      } catch (refreshError) {
        sessionStorage.removeItem("access_token");
        window.location.href = "/login";
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error); // dla innych błędów po prostu odrzucamy promise
  }
);


export default api;
