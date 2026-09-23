import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://partyprintkit.com',
  // dist lives outside the synced folder: the mount does not allow unlink,
  // and Astro rewrites its output directory on every build.
  outDir: process.env.ASTRO_OUT_DIR || './dist',
  cacheDir: process.env.ASTRO_CACHE_DIR || './node_modules/.astro',
  trailingSlash: 'always',
  build: { format: 'directory' },
  image: { responsiveStyles: true },
});
