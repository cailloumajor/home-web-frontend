module.exports = {
  root: true,
  parserOptions: { parser: 'babel-eslint' },
  env: {
    browser: true,
    node: true
  },
  extends: [
    'standard',
    'plugin:vue/recommended'
  ],
  // add your custom rules here
  rules: {
    'no-debugger': process.env.NODE_ENV === 'production' ? 2 : 0,
    'vue/html-end-tags': 1,
    'vue/html-no-self-closing': 1,
    'vue/html-quotes': 1,
    'vue/no-duplicate-attributes': 1,
    'vue/no-template-key': 2,
    'vue/order-in-components': 1,
    'vue/require-v-for-key': 0,
    'vue/v-bind-style': 1,
    'vue/v-on-style': 1
  },
  globals: {}
}
