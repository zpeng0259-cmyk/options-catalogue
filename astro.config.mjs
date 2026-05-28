import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import mdx from '@astrojs/mdx';

export default defineConfig({
  site: 'https://USER.github.io',
  base: '/options-catalogue',
  vite: { plugins: [tailwindcss()] },
  integrations: [mdx()],
});
