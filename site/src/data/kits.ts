import type { ShotId } from './images';
import { routes, type Route } from './site';

export type OccasionCard = { title: string; pieces: string; shot: ShotId; route: Route };

/**
 * Not rendered yet. An occasion appears on the site only once its kit, its
 * photographs and its page exist; a card with nothing behind it is a promise
 * the site cannot keep.
 *
 * Consumer-facing labels only. Search volume, KD, "measured", "core occasion"
 * and any other research figure never reaches the interface: it tells the
 * visitor the page was built for a search engine, and it hands the niche
 * breakdown to competitors for free.
 */
export const occasions: OccasionCard[] = [
  { title: 'Christmas', pieces: 'Banners, table decor, toppers & tags', shot: 'occasion-christmas', route: routes.christmas },
  { title: 'Birthday party', pieces: 'Banners, hats, toppers & signs', shot: 'occasion-birthday', route: routes.birthday },
  { title: 'Graduation', pieces: 'Banners, cap toppers, signs & tags', shot: 'occasion-graduation', route: routes.graduation },
  { title: 'Halloween', pieces: 'Banners, hats, food labels & toppers', shot: 'occasion-halloween', route: routes.halloween },
];

export type PieceCard = { title: string; blurb: string; shot: ShotId; route: Route };

export const pieces: PieceCard[] = [
  { title: 'Party banners', blurb: 'Letters, bunting & garlands', shot: 'piece-banner', route: routes.banners },
  { title: 'Banner letters', blurb: 'Full alphabet, spell anything', shot: 'letters-alphabet-sheet', route: routes.bannerLetters },
  { title: 'Party hats', blurb: 'Print, cut, fold & wear', shot: 'piece-hat', route: routes.partyHats },
];

/** Design catalog; release pages filter this list to products that are actually built. */
export type BannerDesign = {
  id: string;
  name: string;
  title: string;
  swatch: [string, string, string];
  hung: ShotId;
  sheet: ShotId;
  /** The banner on its own: thirteen flags. What the page's own buttons serve. */
  bannerA4: string;
  bannerLetter: string;
  /** The whole kit. Only the "complete kit" buttons may point here. */
  kitA4: string;
  kitLetter: string;
  png: string;
  social: string;
  /** A design ships only once it has its own hung photograph (PRODUCT.md 7.3). */
  released: boolean;
};

/**
 * Order matters: the first design is the default, so it has to be the one with
 * a real vertical sheet photo. The first screen must carry an actual vertical
 * 1000x1500 image, not only a file behind a button.
 *
 * All three ship in the markup and are switched with CSS. Loading them on click
 * would leave one banner on the page for a crawler, and the set of variants is
 * exactly what an AI Overview cannot reproduce.
 */
export const bannerDesigns: BannerDesign[] = [
  {
    id: 'botanical',
    name: 'Botanical',
    title: 'Botanical Birthday Banner',
    swatch: ['#1f5e60', '#eb725b', '#e8dcc4'],
    hung: 'banner-hung-botanical',
    sheet: 'sheet-birthday-banner-botanical',
    bannerA4: '/downloads/birthday-banner-botanical-a4.pdf',
    bannerLetter: '/downloads/birthday-banner-botanical-letter.pdf',
    kitA4: '/downloads/birthday-kit-botanical-a4.pdf',
    kitLetter: '/downloads/birthday-kit-botanical-letter.pdf',
    png: '/downloads/birthday-banner-botanical-1000x1500.png',
    social: '/social/birthday-banner-botanical-1000x1500.jpg',
    released: true,
  },
  {
    id: 'geometric',
    name: 'Geometric',
    title: 'Geometric Birthday Banner',
    swatch: ['#22746f', '#eb725b', '#f4b95d'],
    hung: 'banner-hung-geometric',
    sheet: 'sheet-birthday-banner-geometric',
    bannerA4: '/downloads/birthday-banner-geometric-a4.pdf',
    bannerLetter: '/downloads/birthday-banner-geometric-letter.pdf',
    kitA4: '/downloads/birthday-kit-geometric-a4.pdf',
    kitLetter: '/downloads/birthday-kit-geometric-letter.pdf',
    png: '/downloads/birthday-banner-geometric-1000x1500.png',
    social: '/social/birthday-banner-geometric-1000x1500.jpg',
    released: true,
  },
  {
    id: 'minimal',
    name: 'Minimal',
    title: 'Minimal Birthday Banner',
    swatch: ['#21343b', '#f7f0e3', '#eb725b'],
    hung: 'banner-hung-minimal',
    sheet: 'sheet-birthday-banner-minimal',
    bannerA4: '/downloads/birthday-banner-minimal-a4.pdf',
    bannerLetter: '/downloads/birthday-banner-minimal-letter.pdf',
    kitA4: '/downloads/birthday-kit-minimal-a4.pdf',
    kitLetter: '/downloads/birthday-kit-minimal-letter.pdf',
    png: '/downloads/birthday-banner-minimal-1000x1500.png',
    social: '/social/birthday-banner-minimal-1000x1500.jpg',
    released: false,
  },
];

/** What the kit PDF contains. These are sheets inside one download, not pages,
 *  so they are listed, not linked. */
export const kitPieces = [
  { title: 'Party hats', blurb: 'Two flat templates with fold tabs' },
  { title: 'Cupcake toppers', blurb: '12 round cut-outs per sheet' },
  { title: 'Party signs', blurb: 'Two 5 x 7 in cards' },
  { title: 'Favor tags', blurb: 'Six punch-and-tie tags' },
];

/**
 * The party hat is occasion-neutral, so its files carry no occasion in the
 * name, the same way banner letters do (PRODUCT.md section 6).
 */
export type ArtifactDesign = {
  id: string;
  name: string;
  title: string;
  sheet: ShotId;
  pdfA4: string;
  pdfLetter: string;
  png: string;
  social: string;
  released: boolean;
};

export const partyHatDesigns: ArtifactDesign[] = [
  {
    id: 'botanical',
    name: 'Botanical',
    title: 'Botanical Party Hat',
    sheet: 'sheet-party-hat-botanical',
    pdfA4: '/downloads/party-hat-botanical-a4.pdf',
    pdfLetter: '/downloads/party-hat-botanical-letter.pdf',
    png: '/downloads/party-hat-botanical-1000x1500.png',
    social: '/social/party-hat-botanical-1000x1500.jpg',
    released: true,
  },
  {
    id: 'geometric',
    name: 'Geometric',
    title: 'Geometric Party Hat',
    sheet: 'sheet-party-hat-geometric',
    pdfA4: '/downloads/party-hat-geometric-a4.pdf',
    pdfLetter: '/downloads/party-hat-geometric-letter.pdf',
    png: '/downloads/party-hat-geometric-1000x1500.png',
    social: '/social/party-hat-geometric-1000x1500.jpg',
    released: true,
  },
];
