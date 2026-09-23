# partyprintkit.com

Free printable party decorations. Static site, no backend, no accounts.

```
site/                Astro 7 site
  src/pages/         11 pages
  src/data/          routes, photo slots, products
  scripts/           PDF and raster generators, tests (python)
  public/downloads/  what the download buttons serve
PROJECT.md           ниша, карта ключей, что строим и чего не строим
PRODUCT.md           состав кита, правила печати, гейт релиза
DESIGN.md            интерфейс и правила витрины
DEFECTS.md           статус дефектов с замерами
```

## Работа

```
cd site
npm install
npm run assets     # PDF, растры и иконки; нужен python3 с reportlab, pypdf, pdfplumber, Pillow
npm run dev
npm run build
npm run test       # автотесты продукта и ссылок, гонять после build
```

`output/` не в репозитории: он пересобирается `npm run assets`.

## Два правила, которые держатся кодом

**Никаких исследовательских цифр в интерфейсе.** Объёмы, KD и доли AI Overview не попадают в разметку (`DESIGN.md` §10).

**Навигация показывает только то, что существует.** У каждого маршрута в `src/data/site.ts` флаг `built`; непостроенный отдаётся текстом, а не ссылкой.
