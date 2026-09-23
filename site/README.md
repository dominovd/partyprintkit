# partyprintkit.com

Astro 7, статика, без серверной части.

```
npm install
npm run assets     # PDF, растры и иконки; нужен python3 с reportlab, pypdf, pdfplumber, Pillow
npm run dev
npm run build
npm run test       # автотесты продукта и ссылок, гонять после build
```

Сборка кладёт результат в `dist/`. Если папка проекта смонтирована так, что удаление запрещено, соберите наружу:

```
ASTRO_OUT_DIR=~/ppk-dist npm run build
```

## Что где

| путь | что |
|---|---|
| `src/data/site.ts` | навигация, подвал, маршруты с флагом `built` |
| `src/data/images.ts` | перечень фотослотов: файл, alt, пропорции, бриф на съёмку |
| `src/data/kits.ts` | поводы, артефакты, три дизайна баннера |
| `src/data/pin.ts` | ссылка Pinterest, всегда с вертикальным ассетом |
| `scripts/build-product-pdfs.py` | 24 PDF: три дизайна × кит, баннер, шляпа, алфавит × A4 и Letter |
| `scripts/build-product-previews.py` | вертикальные 1000×1500 и карточки деталей |
| `scripts/build-icons.py` | favicon, apple-touch, 192/512 |
| `scripts/test-product-pdfs.py` | геометрия, шрифты, поля, краска, уникальность |
| `scripts/test-site-downloads.py` | число страниц за кнопкой и отсутствие сирот в `downloads/` |

## Два правила, которые держатся кодом

**Никаких исследовательских цифр в интерфейсе.** Объёмы, KD, доли AIO и слова вроде «measured» не попадают в разметку. Подробнее в `DESIGN.md` §10.

**Один слот, один кадр.** Слот в `images.ts` не берёт кадр другого слота. Отсутствующий файл рендерится плашкой с брифом, а не битой картинкой, поэтому дыры видны на макете. `DESIGN.md` §12.

## Нужные кадры

Плашки на макете перечисляют их сами. Список на сейчас:

| файл | кадр |
|---|---|
| `kit-printing-at-home.png` | лист букв выходит из домашнего принтера, рядом ножницы и шпагат |
| `piece-banner.png` | макро: две-три буквы на шнуре с прищепками |
| `piece-hat.png` | макро: руки сворачивают конус шляпы |
| `piece-topper.png` | макро: топперы воткнуты в капкейки |
| `piece-sign.png` | макро: табличка на подставке рядом с едой |
| `piece-tag.png` | макро: бирка завязана на подарке |
| `banner-hung-minimal.png` | третий дизайн баннера, повешенный |
| `sheet-birthday-banner-geometric.png` | вертикальный 1000×1500 лист геометрического дизайна |
| `sheet-birthday-banner-minimal.png` | вертикальный 1000×1500 лист минимального дизайна |
| `banner-cutting-letters.png` | макро: ножницы по пунктиру 0,25 pt |
| `letters-alphabet-sheet.png` | вертикальный 1000×1500 лист полного алфавита |

`occasion-birthday.png` и `sheet-birthday-banner-botanical.png` сейчас берут существующие кадры (ботанический баннер и общий флэтлей кита). Оба помечены в `images.ts` как временные.

## PDF

`scripts/build-assets.mjs` рисует листы векторно через pdf-lib: пеннант 5×7", пунктир 0,25 pt, две дырки под шнур, подпись `partyprintkit.com` вне зоны реза. Шрифт пока Helvetica; при переходе на Fraunces нужна лицензия на встраивание (`DESIGN.md` §1).
