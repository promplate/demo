import { svelte } from "@sveltejs/vite-plugin-svelte";
import unocss from "unocss/vite";
import { defineConfig } from "vite";

async function getProxies() {
  if (process.env.NODE_ENV !== "production") {
    const BACKEND = "http://localhost:8000/";

    const routes = await fetch(new URL("/openapi.json", BACKEND))
      .then(res => res.json())
      .then(({ paths }) => Object.keys(paths));

    return Object.assign({}, ...["/docs", "/redoc", "/openapi.json", ...routes.map(route => route.replace(/\/\{.*$/, ""))].map(path => ({ [path]: BACKEND })));
  }
}

export default async () => {
  return defineConfig({
    plugins: [unocss(), svelte()],
    server: { proxy: await getProxies() },
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
