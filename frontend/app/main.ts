import { mount } from "svelte";
import App from "./App.svelte";
import "@unocss/reset/tailwind-compat.css";
import "uno.css";

export default mount(App, {
  target: document.body,
});
