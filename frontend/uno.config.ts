import extractorSvelte from "@unocss/extractor-svelte";
import { defineConfig, presetAttributify, presetUno, presetWebFonts, transformerDirectives, transformerVariantGroup } from "unocss";

const config = defineConfig({
  extractors: [extractorSvelte()],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  presets: [presetAttributify(), presetUno({ preflight: "on-demand" }), presetWebFonts({ provider: "bunny", fonts: { mono: "Fira Code" } })],
});

export default config;
