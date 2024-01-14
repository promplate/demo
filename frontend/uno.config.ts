import extractorSvelte from "@unocss/extractor-svelte";
import { defineConfig, presetAttributify, presetUno, transformerDirectives, transformerVariantGroup } from "unocss";

const config = defineConfig({
  extractors: [extractorSvelte()],
  transformers: [transformerDirectives(), transformerVariantGroup()],
  presets: [presetAttributify(), presetUno()],
});

export default config;
