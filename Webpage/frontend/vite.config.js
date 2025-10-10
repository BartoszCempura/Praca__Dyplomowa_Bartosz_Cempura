import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

// https://daisyui.com/docs/install/react/
export default defineConfig({
  plugins: [tailwindcss(), react()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:5000", // Flask backend URL
        changeOrigin: true,
        secure: false, // optional: disable SSL verification if backend uses HTTP
      },
    },
  },
});