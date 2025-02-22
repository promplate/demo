import extractorSvelte from "@unocss/extractor-svelte";
import { defineConfig, presetAttributify, presetWebFonts, presetWind3, transformerDirectives, transformerVariantGroup } from "unocss";

const config = defineConfig({
  extractors: [extractorSvelte()],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  presets: [presetAttributify(), presetWind3({ preflight: "on-demand" }), presetWebFonts({ provider: "bunny", fonts: { mono: "Fira Code" } })],
});

export default config;
