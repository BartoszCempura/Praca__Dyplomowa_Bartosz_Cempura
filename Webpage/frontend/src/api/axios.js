import axios from "axios";

// Tworzymy instancję axios z baseURL "/api", żeby korzystała z proxy Vite
const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true, // pozwala wysyłać ciasteczka (refresh token)
});

export default api;