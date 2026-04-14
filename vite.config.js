import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      // Proxy all /api/* requests to the Flask backend during development
      "/api": {
        target: "http://localhost:5001",
        changeOrigin: true,
      },
    },
  },
});
