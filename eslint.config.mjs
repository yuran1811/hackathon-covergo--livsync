import antfu from '@antfu/eslint-config';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';

export default antfu(
  {
    formatters: {
      html: true,
      css: true,
      markdown: 'prettier',
    },
    stylistic: {
      indent: 2,
      semi: true,
      quotes: 'single',
    },
    javascript: true,
    typescript: true,
    markdown: true,
    jsonc: true,
  },
  {
    ignores: [
      '**/node_modules',
      '**/dist',
      '**/build',
      '**/output',
      '**/public',
      '**/coverage',
      '**/test-results',
      '**/generated/prisma',
      'apps/api',
      'pnpm-lock.yaml',
    ],
  },
  {
    rules: {
      'new-cap': 'off',
      'vars-on-top': 'off',
      'no-console': 'off',
      'no-empty': 'off',
      'no-restricted-globals': 'off',

      'regexp/no-unused-capturing-group': 'off',
      'regexp/no-useless-escape': 'off',
      'eslint-comments/no-unlimited-disable': 'off',
      'node/prefer-global/process': 'off',
      'unused-imports/no-unused-vars': 'warn',

      'antfu/consistent-chaining': 'off',
      'antfu/consistent-list-newline': 'off',
      'antfu/if-newline': 'off',
      'antfu/top-level-function': 'off',

      'style/brace-style': 'off',
      'style/comma-dangle': 'off',
      'style/member-delimiter-style': 'off',
      'style/operator-linebreak': 'off',
      'style/quote-props': 'off',

      'ts/ban-ts-comment': 'off',
      'ts/no-empty-object-type': 'off',
      'ts/no-explicit-any': 'off',
      'ts/no-require-imports': 'off',
      'ts/no-unused-vars': 'off',
      'ts/strict-boolean-expressions': 'off',
    },
  },
  {
    files: ['**/*.{ts,tsx}'],
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
  eslintPluginPrettierRecommended,
  {
    rules: {
      'prettier/prettier': 'error',
    },
  },
  {
    files: ['**/*.md'],
    rules: {
      'prettier/prettier': ['warn', { parser: 'markdown' }],
    },
  },
);
