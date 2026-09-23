import type { APIRoute } from 'astro';
import { site } from '../data/site';

/**
 * The sitemap is derived from the page files themselves, not from a hand-kept
 * list. A page that is not built cannot appear here, and a page that is built
 * cannot be forgotten.
 *
 * No lastmod and no priority: a build date is not a content date, and Google
 * ignores priority. Better to say nothing than to say something untrue.
 */
const pages = import.meta.glob('./**/*.astro');

/** Pages that exist but do not belong in a sitemap. */
const EXCLUDED = new Set(['/404/']);

function toUrl(file: string): string {
  const path = file
    .replace(/^\.\//, '')
    .replace(/\.astro$/, '')
    .replace(/(^|\/)index$/, '');
  return path ? `/${path}/` : '/';
}

export const GET: APIRoute = () => {
  const urls = Object.keys(pages)
    .map(toUrl)
    .filter((url) => !EXCLUDED.has(url))
    .sort((a, b) => a.localeCompare(b));

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map((url) => `  <url><loc>${new URL(url, site.origin).href}</loc></url>`).join('\n')}
</urlset>
`;

  return new Response(body, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
};
