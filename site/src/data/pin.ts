import { site } from './site';

/**
 * Pinterest always gets the vertical 1000x1500 asset, never the horizontal
 * hero. Same file the Image pack indexes.
 */
export function pinUrl(opts: { path: string; media: string; description: string }) {
  const params = new URLSearchParams({
    url: new URL(opts.path, site.origin).href,
    media: new URL(opts.media, site.origin).href,
    description: opts.description,
  });
  return `https://www.pinterest.com/pin/create/button/?${params.toString()}`;
}
