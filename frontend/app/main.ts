import App from "./App.svelte";
import "@unocss/reset/tailwind-compat.css";
import "uno.css";

const app = new App({
  target: document.getElementById("app")!,
});

export default app;
