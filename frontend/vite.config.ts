import { svelte } from "@sveltejs/vite-plugin-svelte";
import unocss from "unocss/vite";
import { defineConfig } from "vite";

export default async () => {
  const BACKEND = "http://localhost:8000/";

  const routes = await fetch(new URL("/openapi.json", BACKEND))
    .then(res => res.json())
    .then(({ paths }) => Object.keys(paths));
  const proxy = Object.assign({}, ...["/docs", "/redoc", "/openapi.json", ...routes.map(route => route.replace(/\/\{.*$/, ""))].map(path => ({ [path]: BACKEND })));

  return defineConfig({
    plugins: [unocss(), svelte()],
    server: { proxy },
    build: {
      rollupOptions: {
        output: {
          assetFileNames: "[name].[ext]",
          chunkFileNames: "[name].js",
          entryFileNames: "[name].js",
        },
      },
    },
  });
};
