import antfu from "@antfu/eslint-config";

export default antfu({
  svelte: true,
  typescript: true,
  stylistic: {
    quotes: "double",
    semi: true,
  },
  formatters: true,
  jsonc: false,
  unocss: true,
  rules: {
    "perfectionist/sort-imports": "error",
    "node/prefer-global/process": "off",
  },
});
