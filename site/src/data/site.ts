export const site = {
  name: 'PartyPrintKit',
  origin: 'https://partyprintkit.com',
  tagline: 'Print the pieces. Make the party.',
  blurb:
    'Free, coordinated party decorations made to print, cut and celebrate. No editor, sign-up or paywall.',
};

/**
 * Routes carry a `built` flag. Anything not built yet renders as plain text
 * instead of a link, so navigation never promises a page that 404s and the
 * remaining work stays visible in the markup.
 */
export type Route = { href: string; label: string; built: boolean };

export const routes = {
  home: { href: '/', label: 'Home', built: true },
  occasions: { href: '/occasions/', label: 'Occasions', built: false },
  printables: { href: '/printables/', label: 'Printables', built: true },
  printingGuide: { href: '/printing-guide/', label: 'Printing guide', built: true },
  banners: { href: '/banners/', label: 'Banners', built: true },
  bannerLetters: { href: '/banners/letters/', label: 'Printable banner letters', built: true },
  partyHats: { href: '/party-hats/', label: 'Party hats', built: true },
  toppers: { href: '/cupcake-toppers/', label: 'Cupcake toppers', built: false },
  signs: { href: '/party-signs/', label: 'Party signs', built: false },
  tags: { href: '/favor-tags/', label: 'Favor tags', built: false },
  birthday: { href: '/birthday/', label: 'Birthday', built: false },
  birthdayBanners: { href: '/birthday/banners/', label: 'Birthday banners', built: true },
  christmas: { href: '/christmas/', label: 'Christmas', built: false },
  graduation: { href: '/graduation/', label: 'Graduation', built: false },
  halloween: { href: '/halloween/', label: 'Halloween', built: false },
  about: { href: '/about/', label: 'About', built: true },
  terms: { href: '/terms/', label: 'Terms of use', built: true },
  contact: { href: '/contact/', label: 'Contact', built: true },
} satisfies Record<string, Route>;

/**
 * One "Printables" entry, not five. The artefact hubs live behind it.
 * Five top-level items would grow with every artefact and would imply a
 * ranking the site does not have.
 */
/**
 * Navigation lists only what exists. An entry is added the day its page ships,
 * not the day it is planned: a menu half made of dead text reads as an
 * abandoned site on every page a visitor lands on.
 */
export const nav: Route[] = [routes.printables, routes.printingGuide];

export const footerColumns = [
  { title: 'Printables', links: [routes.banners, routes.bannerLetters, routes.partyHats] },
  { title: 'PartyPrintKit', links: [routes.printingGuide, routes.about, routes.terms, routes.contact] },
];
