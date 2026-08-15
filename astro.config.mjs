import { defineConfig } from 'astro/config';

const isProd = process.env.NODE_ENV === 'production' || process.argv.includes('build');

// https://astro.build/config
export default defineConfig({
  output: 'static',
  site: 'https://nutflaggers.github.io',
  base: isProd ? '/website/' : '/',
  markdown: {
    shikiConfig: {
      theme: 'github-dark-dimmed',
      wrap: true
    }
  }
});
