import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { quasar, transformAssetUrls } from "@quasar/vite-plugin";

import { fileURLToPath, URL } from "url";

export default defineConfig({
  root: "app",
  build: { sourcemap: true, outDir: "../dist", emptyOutDir: true },
  resolve: {
    alias: [
      {
        find: "@",
        replacement: fileURLToPath(new URL("./app", import.meta.url)),
      },
    ],
  },
  plugins: [
    vue({
      template: { transformAssetUrls },
    }),

    quasar({}),
  ],
});
