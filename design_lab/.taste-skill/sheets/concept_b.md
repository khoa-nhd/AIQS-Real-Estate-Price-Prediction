# DIRECTION SHEET — The well-kept board
seed 2126786358 · drawn 2026-10-14 · sector saas · tone technical
Brief: Vietnamese house price estimator: enter a house's details, get an estimated price in ty dong from a trained model, stated as an estimate

| | |
| --- | --- |
| Direction | The well-kept board |
| Hero | Name band and rails |
| Type | Albert Sans |
| Colour | Cool grey, cobalt |
| Sections | stats (Photograph with figure tiles) → proof (Large marks on tiles) → about (Wide photo, colour tile, facts) |
| Motion | Edge-to-edge marquee |
| Photographs | the "Architecture" set, as atmosphere |

This is the direction for this build. Adopt it. Do not blend it with the layout you would have made anyway,
and do not redraw because it is unfamiliar: unfamiliar is the point. Redraw a slot only when it conflicts
with a stated brand constraint or needs an asset that does not exist, and say why in your report.

The parts of this sheet were written separately and will disagree in small ways. Settle every disagreement in this order:
**house rules** (including type no smaller than 13px and body text of 16px or more) → **the direction** (the idea, the composition habits, where the
one accent goes) → **the type system and the palette** (which face does which job, the five size steps, which colour is the ground and where the
accent goes) → **the hero blueprint** → **the section blueprints**. Under each blueprint below, "Adjusted for this page" lists where it disagrees.
In practice: take geometry from blueprints (columns, proportions, what sits where) and take everything else from above them. Map every size a
blueprint names onto one of your five type steps instead of adding a sixth. Use one button shape, one corner radius and one pair of page margins on
the whole page, whatever individual blueprints say. If a blueprint names a kind of typeface (a light serif, a heavy grotesk), use the dealt face.

## 1. The idea
The whole page is a board of tiles fitted edge to edge with narrow gaps, like a tidy desk seen from above. Each tile is one thing: the name, a statement, a photograph, a number, a link, a short list. There is no hero and no sequence of bands; the page is one continuous composition that the eye roams. It suits subjects with many small true things to show (a studio with work, writing, clients and news; a product with several distinct capabilities) and it replaces the generic bento by having real content in every tile and a strict system for sizes.

Before anything else, write one sentence in your notes: "On this page, <the subject's own material> becomes <the device>."
Fill the first blank from your inventory of what only this client has (its name and what it means, its street, its numbers, its
constraint), then put the nearest competitor in the sentence: if it still works, the idea is the category's, not the client's.
Then name the one live thing the visitor can do on the page (SKILL.md step 4).

## 2. Composition
A 12-column grid with 8px gaps and 8–12px outer margins, filled completely, no empty cells. Tiles use only four sizes (for example 6×4, 6×2, 3×2, 3×4 in column × row units of about 90px). Every tile is a flat filled rectangle: ground colour one step from the page, or a palette colour, or a photograph covering it. One radius everywhere (0, or 6–10px). The first screen contains: a name tile (the name at display size, the largest type on the page) with the wordmark set large, a statement tile with the description at 28–40px, two or three image tiles and one action tile in the accent colour. Text inside tiles is top-left aligned with 20–24px padding and never centred. Below the first screen the board continues with the same sizes; the last row is the footer made of tiles.

## 3. Type — Albert Sans
A geometric grotesque with Scandinavian restraint: round letters, even colour, nothing decorative. Suits logistics, health, property and corporate sites that need to look clear and dependable.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```
- Display: **Albert Sans** — weight 600 · tracking -0.035em · leading 1.0 · sentence case
- Text: **Albert Sans** — 400 for body, 500 for emphasis · leading 1.5 · tracking 0
```css
:root {
  --step-small: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --step-body: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
  --step-lead: clamp(1.25rem, 1.1rem + 0.7vw, 1.625rem);
  --step-head: clamp(2rem, 1.3rem + 3.2vw, 4rem);
}
```
One grotesk in two weights. Inside tiles: a large size for single statements, a small size for lists. No uppercase labels in tile corners.
The direction decides sizes and how many of them; the type system decides how this face is set. Where the two give different tracking or leading, use the values of the type system: they are tuned to this face.
The display size itself comes from the hero blueprint below.

## 4. Colour — Cool grey, cobalt
```css
:root {
  --bg: #eef0f3;
  --surface: #e2e5ea;
  --ink: #0b0c0e;
  --muted: #5d6470;
  --accent: #1f2de6;
  --accent-ink: #ffffff;
  --field-1: #1f2de6;  --field-1-ink: #ffffff;
}
```
Cool pale grey holds the page with near-black type and nothing else tinted. Cobalt starts as the button and one highlighted sentence, takes one whole section as a flat field with white text, then returns as a single button block.
Page ground, tile ground one step lighter or darker, and one or two palette colours on selected tiles. Photographs supply the rest.

## 5. Imagery
**This subject is software and there are no screenshots, so its pictures are its own interface.** Wherever this sheet says photograph, image or object, build a believable fragment of the product in HTML at real size (real labels, numbers that add up, one item hovered or selected), put the attribute `data-ui` on its root, and crop or scale it the way the blueprint treats a photograph: a full-bleed close crop, a tile, the fixed half of a split. Where a fragment makes no sense, use a flat colour field with type on it. Never a fake dashboard of grey bars, never a device frame. If the product works on something physical (ships, plants, buildings, a city), one real picture of that world can carry a section: find it with `node D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/.claude/skills/design-taste-frontend/scripts/assets.mjs "<that world>"`, download it with `--get`, credit it on the page, and never let it pass for the product or its customers.

Photographs fill whole tiles with `object-fit: cover`; choose images that crop well to both wide and tall tiles.

**Floor (the inspector checks it):** at least four real pictures on the page, usually six to twelve; SVG drawings do not count. One moving picture where an honest clip exists: `node <skill>/scripts/assets.mjs --video "<query>"`, used as a muted loop with a poster frame. Whatever this direction says about pictures, it is carried out with real ones.

Optional atmosphere, two at most, from the "Architecture" set (structure, lines, bridges, facades and building interiors). The page does not need them.
Order of preference for imagery: (1) the project's own photographs and product shots; (2) images you generate, if an image tool is
available; (3) real pictures of the subject's world found in the open collections (assets.mjs, downloaded and credited on the page);
(4) drawings of the subject in code; (5) these. They are real photographs (Unsplash licence, served by picsum.photos) of places, light and
texture. They are atmosphere, never a stand-in for a specific product, dish, person or interface. List the ones you use in your report so
they can be replaced.
- `https://picsum.photos/id/870/1600/1000` — White lighthouse with its lamp lit against a deep blue starry sky · mid tone · deep blue, white, warm orange · calm area: right · native portrait · photo: Joshua Hibbert
- `https://picsum.photos/id/946/1600/1000` — Yellow brick house front with a dark green door and window · mid tone · ochre yellow, dark green, charcoal · native landscape · photo: Padurariu Alexandru
- `https://picsum.photos/id/508/1600/1000` — Tall pointed vaults and pale columns of a church interior · light tone · cream, warm grey, soft orange · native portrait · photo: Jeff Sheldon
- `https://picsum.photos/id/1081/1600/1000` — Stepped white modern building corner rising into a pale blue sky · light tone · white, pale blue, soft grey · calm area: top · native landscape · photo: Julien Moreau
The last two path numbers are width and height: request the exact crop you render (`/1200/1500` for a 4:5 portrait, `/2400/1350` for a hero) and
add `?grayscale` to desaturate. Use at most two. Always set `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).
Other sets that fit this brief: fog-and-quiet, sky-and-space — `node draw.mjs --photos <set>` prints one in full; `--photos list` shows all sets. Taking photographs from another set is your call and is not a redraw; keep them to one light and one treatment.

## 6. Hero — Name band and rails
One viewport filled completely with tiles on 8px gaps and 8px margins. Across the top, a band tile 170px tall holds the name on one line at clamp(140px, 14.4vw, 220px), heavy, tracking -0.04em, centred and deliberately wider than the band so both ends are cropped by the tile's edges (overflow: hidden, white-space: nowrap). Under it a row of four equal tiles, 64px tall, each holding one text link at 16px, top-left aligned. The remaining 62% of the height is three columns. Left rail (columns 1-2): two stacked tiles, a portrait photograph above and a short list of five facts below. Centre (columns 3-10): one large photograph tile, object-fit: cover, with a statement tile in the ground tone laid along its bottom third holding one sentence at clamp(24px, 2.4vw, 36px), top-left aligned on 24px padding. Right rail (columns 11-12): a full-height stack of five flat colour tiles, a light-to-dark run from the palette; the lowest takes the accent colour and holds the single action, the others each carry one short fact at 15px.

On a phone: Tiles restack in two columns with 6px gaps. The name band stays full width: 26vw type cropped at both sides in a 110px band. The four link tiles become a two-by-two block. The large photograph tile follows at full width, 4:3, with the statement tile under it at 6vw. The colour rail becomes a horizontal row of five short tiles, the action tile last and twice as wide.
Headline: The name on one cropped line, any length, plus one sentence of up to 60 characters in the statement tile.

Adjusted for this page:
- It sets a sentence large over several lines: jurors read that as a long headline. Either cut it to a two-line headline at display size, or keep it a statement at 36px or less on three lines (24px, four lines on a phone).

## 7. Sections, in order
Each is a composition to rebuild with this project's content. Keep the geometry; change the subject. Re-order or drop a
section when the argument of the page needs it (see references/copy.md), never to fall back to a card grid.

### 1. stats — Photograph with figure tiles (mosaic)
A mosaic without gutters spanning the full width, about 66vw tall in total. A single photograph fills the left two-thirds at roughly 1:1 with object-fit: cover and square corners. The right third is split into two stacked flat colour tiles of equal height, in two palette colours that differ clearly in lightness as well as hue. Each tile carries one figure at clamp(56px, 5.6vw, 96px) in its top-left corner, 28px in from the edges, with a two-line caption at 17px directly beneath it; the rest of the tile is empty colour, which is the point. Photograph and tiles touch, with no gaps and no rounding. The heading, two to four words at 32–40px, sits above the mosaic's left edge with 40px beneath, or is left out when the section follows a text page whose title already introduces it. Never add a third tile; with three figures choose another layout.
On a phone: The photograph comes first, full-bleed at 4:3. The two colour tiles follow side by side as squares, each 50vw, with the figure at 13vw top-left and the caption at 15px beneath. No gaps between any of the three pieces.

### 2. proof — Large marks on tiles (grid)
A board of filled tiles, four across and two or three rows deep, with 8px gaps, spanning the full content width. Each tile is about 3:2, one step lighter or darker than the page ground, with no border. A tile holds one supplied logo, shown far larger than a usual logo strip: about 72px tall, centred, in the page ink as a single-colour SVG. When no logo files exist, the tile holds the name instead, set at 28–32px bold, top-left with 24px padding; never draw a mark. One tile, twice the width of the others and placed first, is in the accent colour and carries the heading: two to four words at about 3vw, top-left. Tile corners follow the page's one radius, or the page's motif shape if it has one. Tiles sit still; there is no hover lift.
On a phone: Two tiles per row with 6px gaps, logos at 44px tall. The heading tile runs full width first, about 120px tall. Show eight tiles at most so the board stays under one and a half screens. Names set in type drop to 20px.

### 3. about — Wide photo, colour tile, facts (mosaic)
Top: a heading of two to four words at clamp(40px, 4vw, 60px) on the left margin, then 24px below it a three-line lead paragraph at 21–22px across columns 1–6. 72px lower, two tiles sit side by side with a 16px gap. The left tile spans columns 1–8: a landscape photograph at 16:10 with one radius (0 or 10px). A short paragraph of up to 35 words at 16px is set in a solid paper-colour block 320px wide with 20px padding, placed over the photograph's top-right corner and flush with both edges. The right tile spans columns 9–12 and is a flat palette colour, 60% of the photograph's height: it holds a simple inline SVG outline of the region or the floor plan as one filled shape, with one solid dot marking the location. Under the colour tile, four label and value pairs at 14px in a two-by-two grid: altitude, distance, season, local time.
On a phone: Heading at 9vw, lead at 18px. The photograph goes full width at 4:3 and its overlaid paragraph moves beneath it as ordinary text. The colour tile follows at full width and 3:2, and the four label and value pairs sit under it in two columns.

Adjusted for this page:
- It sets text at 10px: use your small step (13px or more) instead.

## 8. Motion — Edge-to-edge marquee
One line of very large type travels sideways across the full width at a slow constant speed, as a band between two sections or as the closing statement. Linear timing, duplicated content for a seamless loop, paused on hover and under reduced motion. One marquee per page, carrying real words (the name, the claim), never a list of buzzwords.
This is the signature move, the one loud moment. Around it the page still needs the rest of the motion layer (SKILL.md step 9): an entrance for the parts of every section, feedback on every control, and one moving picture. The inspector fails a page that barely moves. Recipes: references/motion.md.

## 9. Where the richness comes from
The fit. A full board with consistent gaps and varied tile contents is satisfying in the way a packed suitcase is.

## 10. How this direction goes wrong
Tiles are filled, never outlined, and never carry shadows. Do not put an icon and a two-line feature blurb in every tile; vary what tiles hold. Decide the phone layout as its own board: two columns, tiles re-ordered so the name and statement lead.

## 11. Real references
Studied sites that work this way. Take the principle, never the specifics: no names, copy, images or signature assets of theirs.
- **Aspen Search** (Awwwards Site of the Day, studied score 8.2) `aww-aspen-search`
  Idea: The page is a ruled tile system with no margins: the two-word name is split across cells that alternate type, dithered canvas, black and one mint green.
  Hero: A 60px top bar ruled into cells: black logo square, local time, nav links starting at the centre line, a theme toggle and a black contact cell flush right. Below, the viewport is a two-by-two grid divided by 1px black lines, no outer margin. Top-left is white with the first word of the name at 12.5vw, weight 450, sitting bottom-left. Top-right and bottom-left cells hold a black-and-white dithered canvas crossed by large pale-grey blade shapes that ignore cell borders. The bottom-right quadrant splits into a black cell (24px white summary, mono caps action row at its base) and a mint cell (second statement, client-logo marquee along the bottom).
  Worth taking: Rule the whole viewport into cells with 1px lines and no page margin, then give the nav, the headline, the summary and the proof each its own cell with a flat fill.
- **Oimachi** (Awwwards Site of the Day, studied score 7.1) `aww-oimachi`
  Idea: A studio homepage that behaves like a dense dashboard: work, posts, experiments and testimonials tiled edge to edge with 8px gutters instead of spaced-out sections.
  Hero: Charcoal ground (#181818) with only 8px side margins. Top-left: a round logo, then five tiny black rectangular chips with bold white 13px labels; top-right a contact chip and a theme toggle. The headline starts at the left margin about 160px down: two lines of light grotesk at 52px (3.6vw), tight tracking, with one word in italic serif. From 280px to the bottom edge runs a three-part row: two tall images butted together (each about 535x610px: a hand holding a phone on black, a man in a printed tee) and a 330px sidebar of blog posts, each a bold 14px title, two grey truncated lines and a small-radius thumbnail.
  Worth taking: Shrink page margins and gutters to 8px and tile media edge to edge so a portfolio reads as a working dashboard rather than a brochure.
- **Rows** (One Page Love, studied score 7.5) `opl-rows`
  Idea: Radical understatement: a product about simple lists is sold with a 27px headline, 12px copy and a column of small live demos, each proving one interaction.
  Hero: Warm off-white page, almost empty. Everything hangs on one vertical line 27% in from the left. A small striped-letter logo mark sits there near the top; 220px lower comes a two-line headline at only 27px (under 2vw), then three lines of 13px body about 370px wide, then a near-black rectangular button with 4px corners beside a text link with an arrow. A single grey sign-in link sits in the top-right corner; there is no navigation bar. More than 80% of the viewport is blank. At the bottom edge the first feature module peeks in: grey demo panel left, short text column right.
  Worth taking: Set the headline at near-body size (under 2vw) and let empty space, not scale, give it importance.
Full notes on any of them: `node draw.mjs --site <id>`.

## Always
Headlines two lines or fewer at every width. No eyebrow labels, no monospace, no 01/02/03, no thin rules, no gradients, no shadows at rest,
no cream-and-terracotta, no violet. `inspect.mjs` measures all of it.

Saved to D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/design_lab/.taste-skill/direction.json · reprint with `node draw.mjs --show`
