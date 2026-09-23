/**
 * Photo slots.
 *
 * Rule: one slot = one shot. A slot never borrows another slot's frame.
 * The page sells variety; the same crop repeated across five cards reads as
 * "they only have one kit". `brief` is the shooting instruction and it is what
 * the placeholder prints while the file is missing, so gaps stay visible.
 *
 * Files live in src/assets/photos/<file>.
 */
export type Shot = { file: string; alt: string; ratio: string; brief: string; missing?: true };

export const shots = {
  'home-hero-birthday-table': {
    file: 'home-hero-birthday-table.png',
    alt: 'Printed birthday banner, paper party hats, cupcake toppers and a table sign assembled at home',
    ratio: '3 / 2',
    brief: 'Wide interior, the whole assembled birthday kit on a sideboard. Hero only.',
  },
  'kit-printing-at-home': {
    file: 'kit-printing-at-home.png',
    alt: 'A printed sheet of banner letters coming out of a home inkjet printer beside scissors and twine',
    ratio: '4 / 5',
    brief:
      'Home printer on a desk, a sheet of banner letters half fed out, scissors and twine beside it. Proves "print at home" and keeps the flat lay exclusive to the featured kit block.',
  },
  'kit-sheets-flatlay-vertical': {
    file: 'kit-sheets-flatlay-vertical.png',
    alt: 'Printable birthday kit sheets laid out: banner letters, party hat template, cupcake toppers, a table sign and favor tags',
    ratio: '2 / 3',
    brief:
      'Vertical 1000x1500 flat lay of every sheet in the kit. The indexed asset: og:image, Image pack, Pinterest. Used once per page.',
  },
  'occasion-christmas': {
    file: 'occasion-christmas.png',
    alt: 'Printed Merry Christmas banner above a table with paper trees, cupcake toppers and gift tags',
    ratio: '4 / 3',
    brief: 'Christmas kit in a room. Occasion card only.',
  },
  'occasion-birthday': {
    file: 'occasion-birthday.png',
    alt: 'Printed Happy Birthday banner on a wall with paper party hats and cupcake toppers below',
    ratio: '4 / 3',
    brief:
      'Birthday kit in a room, different room and angle from the hero. Currently borrowing the botanical banner frame; replace with a dedicated birthday occasion shot.',
  },
  'occasion-graduation': {
    file: 'occasion-graduation.png',
    alt: 'Printed Congrats Grad banner with a card, gift bag and favor tags',
    ratio: '4 / 3',
    brief: 'Graduation kit in a room. Occasion card only.',
  },
  'occasion-halloween': {
    file: 'occasion-halloween.png',
    alt: 'Printed Happy Halloween banner with paper hats, bat cutouts and cupcake toppers',
    ratio: '4 / 3',
    brief: 'Halloween kit in a room. Occasion card only.',
  },
  'piece-banner': {
    file: 'piece-banner.png',
    alt: 'Close-up of printed banner letter flags with the dashed cut line and hanging holes',
    ratio: '4 / 5',
    brief:
      'Product card rendered from the kit PDF. Replace with a macro of two or three cut flags on twine once a set has been printed and photographed.',
  },
  'piece-hat': {
    file: 'piece-hat.png',
    alt: 'Printed party hat template sheet with the glue tab marked',
    ratio: '4 / 5',
    brief:
      'Product card rendered from the kit PDF. Replace with a macro of hands rolling a printed cone, once photographed from a real print.',
  },
  'piece-topper': {
    file: 'piece-topper.png',
    alt: 'Printed cupcake topper sheet with twelve cut-out circles',
    ratio: '4 / 5',
    brief:
      'Product card rendered from the kit PDF. Replace with a macro of the toppers standing in cupcakes, once photographed from a real print.',
  },
  'piece-sign': {
    file: 'piece-sign.png',
    alt: 'Printed party sign sheet reading CAKE THIS WAY',
    ratio: '4 / 5',
    brief:
      'Product card rendered from the kit PDF. Replace with a macro of the sign in an easel, once photographed from a real print.',
  },
  'piece-tag': {
    file: 'piece-tag.png',
    alt: 'Printed favor tag sheet with six punch-and-tie tags',
    ratio: '4 / 5',
    brief:
      'Product card rendered from the kit PDF. Replace with a macro of one tag tied to a gift, once photographed from a real print.',
  },
  'banner-hung-botanical': {
    file: 'banner-hung-botanical.png',
    alt: 'Free printable happy birthday banner with botanical leaves, strung on twine above a sideboard',
    ratio: '4 / 3',
    brief: 'Botanical design variant, hung and finished.',
  },
  'banner-hung-geometric': {
    file: 'banner-hung-geometric.png',
    alt: 'Printable happy birthday banner in the geometric design, hung in two rows above a wooden sideboard',
    ratio: '4 / 3',
    brief: 'Geometric design variant, hung and finished.',
  },
  'banner-hung-minimal': {
    file: 'banner-hung-minimal.png',
    alt: 'Happy birthday banner printable in a minimal black and cream design hung across a plain wall',
    ratio: '4 / 3',
    brief: 'Minimal design variant, hung and finished. Same room family as the other two, different design.',
    missing: true,
  },
  'sheet-birthday-banner-geometric': {
    file: 'sheet-birthday-banner-geometric.png',
    alt: 'Happy birthday printable banner sheet, geometric design, thirteen letter flags ready to cut',
    ratio: '2 / 3',
    brief:
      'Vertical 1000x1500 straight-on shot of the printed geometric letter sheet, dashed cut lines and hanging holes readable. This is the indexed asset for the combination page.',
  },
  'sheet-birthday-banner-botanical': {
    file: 'sheet-birthday-banner-botanical.png',
    alt: 'Birthday banner printable sheet, botanical design, letter flags with cut lines and hanging holes',
    ratio: '2 / 3',
    brief:
      'Vertical 1000x1500 straight-on shot of the printed botanical letter sheet. Currently the full kit flat lay, which is the botanical set; replace with a banner-only frame.',
  },
  'sheet-birthday-banner-minimal': {
    file: 'sheet-birthday-banner-minimal.png',
    alt: 'Happy birthday banner printable pdf sheet, minimal design, plain letter flags on cream paper',
    ratio: '2 / 3',
    brief: 'Vertical 1000x1500 straight-on shot of the printed minimal letter sheet.',
    missing: true,
  },
  'banner-cutting-letters': {
    file: 'banner-cutting-letters.png',
    alt: 'Scissors cutting a printed banner letter along the dashed cut line',
    ratio: '4 / 5',
    brief: 'Macro: scissors on the dashed 0.25 pt cut line of a printed letter sheet.',
    missing: true,
  },
  'sheet-party-hat-botanical': {
    file: 'sheet-party-hat-botanical.png',
    alt: 'Printable party hat template sheet in the botanical design, two true-size cones with the glue tab marked',
    ratio: '2 / 3',
    brief:
      'Product card rendered from the party hat PDF. Replace with a straight-on shot of the printed sheet once one has been printed and photographed.',
  },
  'sheet-party-hat-geometric': {
    file: 'sheet-party-hat-geometric.png',
    alt: 'Free printable party hat template in the geometric design, cut, roll and glue the tab',
    ratio: '2 / 3',
    brief:
      'Product card rendered from the party hat PDF. Replace with a straight-on shot of the printed sheet once one has been printed and photographed.',
  },
  'letters-alphabet-sheet': {
    file: 'letters-alphabet-sheet.png',
    alt: 'Printable banner letters sheet with the full alphabet, numbers and punctuation flags',
    ratio: '2 / 3',
    brief:
      'Vertical 1000x1500 flat lay of the full alphabet sheet: A to Z, 0 to 9, ampersand and exclamation mark, cut lines visible.',
  },
} satisfies Record<string, Shot>;

export type ShotId = keyof typeof shots;
