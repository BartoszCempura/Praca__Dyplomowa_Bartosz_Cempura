import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

// https://daisyui.com/docs/install/react/
export default defineConfig({
  plugins: [tailwindcss(), react()],
});