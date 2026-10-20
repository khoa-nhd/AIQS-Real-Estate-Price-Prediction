# DIRECTION SHEET — The name as a monument
seed 223101500 · drawn 2026-10-14 · redraws: 1 · sector real-estate · tone luxury
Brief: Vietnamese house price estimator: enter a house's details, get an estimated price in ty dong from a trained model, stated as an estimate

| | |
| --- | --- |
| Direction | The name as a monument |
| Hero | Stacked name, two inks |
| Type | Anton / Work Sans |
| Colour | Rose grey, green |
| Sections | how-it-works (Photographs down a diagonal) → proof (Names running off the edges) → about (Side facts, wide paragraph) |
| Motion | Masked headline |
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
The name is the headline. Set it so large that it becomes architecture: as wide as the viewport, cropped by an edge, or stacked to fill the screen. Nothing else on the first screen competes; the description of what this is drops to a single small sentence. The idea comes from treating the name's letters as material. Ask what the subject can do to its own name: a photograph of the work sits inside a counter or replaces a letter, the name repeats down the page like a reel, the letters are split to opposite corners and the page happens between them. In the study this was the single most common device among sites scoring 7.5 or more.

Before anything else, write one sentence in your notes: "On this page, <the subject's own material> becomes <the device>."
Fill the first blank from your inventory of what only this client has (its name and what it means, its street, its numbers, its
constraint), then put the nearest competitor in the sentence: if it still works, the idea is the category's, not the client's.
Then name the one live thing the visitor can do on the page (SKILL.md step 4).

## 2. Composition
First screen: the wordmark spans 88–100% of the viewport width (font-size 16–24vw, set with a clamp so it never wraps), anchored either to the bottom edge with its descenders nearly touching it, or dead centre with everything else pushed to the corners. One line of supporting text at 16–20px sits in a corner on a shared margin; navigation is three or four words in the opposite corner. After the hero the page is deliberately small and calm: a narrow text column or a simple two-column grid, so the contrast with the monument holds. The name returns once more at full width as the footer, in the inverse colours. Margins are tight (20–32px) so the type reaches the edges. Two type sizes do nearly all the work: the monument and a small text size, with one mid size for section headings.

## 3. Type — Anton / Work Sans
Compressed heavy capitals stacked tight, with a neutral grotesque kept small beneath. Suits fashion drops, sport, nightlife and any page built as a poster.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton:wght@400&family=Work+Sans:wght@400;600&display=swap" rel="stylesheet">
```
- Display: **Anton** — weight 400 (single heavy cut) · tracking -0.01em · leading 0.86 · uppercase
- Text: **Work Sans** — 400 for body, 600 for links and short emphasis · leading 1.5 · tracking 0
```css
:root {
  --step-small: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --step-body: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
  --step-lead: clamp(1.25rem, 1.1rem + 0.7vw, 1.625rem);
  --step-head: clamp(2.5rem, 1.2rem + 5vw, 5.5rem);
}
```
One family. The display cut must survive enormous sizes: tight tracking (-0.04 to -0.07em), leading 0.8–0.9, optical kerning on. Section headings are modest (28–40px) on purpose.
The direction decides sizes and how many of them; the type system decides how this face is set. Where the two give different tracking or leading, use the values of the type system: they are tuned to this face.
The display size itself comes from the hero blueprint below.

## 4. Colour — Rose grey, green
```css
:root {
  --bg: #ebe5e3;
  --surface: #e1dad7;
  --ink: #2b2622;
  --muted: #6a615d;
  --accent: #0f7d45;
  --accent-ink: #ffffff;
}
```
A single rosy grey covers the page from top to bottom with brown-black text and grey secondary lines; images are kept greyscale. Green appears only on the current-page link and on one button in the footer.
Two values carry the page (ground and ink). The accent, if used at all, appears on one thing only: the single action or the inset image frame. The footer inverts ground and ink.

## 5. Imagery
**The project has no photographs of its own yet.** First choice: **real pictures of the subject's world from the open collections**: its city and street in old postcards and photographs, an old map of the neighbourhood, its materials up close, its trade in engravings, museum objects of its kind (references/imagery.md §3). Start with `node D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/.claude/skills/design-taste-frontend/scripts/assets.mjs "details"`, then queries from your inventory (its street, its materials, its trade's tools and history). Download what you use into the project with `--get` and credit every one on the page (`--credits` prints the footer line). They show the world around the client, never the client's own room, dish, product, person or team. Second, for what no honest picture exists of: draw the subject's own things in code, large, in one flat graphic language and the palette's real colours (its tiles, its windows, its objects; references/imagery.md §8). Third: the dealt photographs, only where an honestly generic picture fits (the sea, the weather, a material), never one a visitor could take for the thing itself and never an unrelated scene. One treatment for all of them. If this direction is built on photographs, plan the set before building (four to six pictures of one family) and reuse them at different crops and scales instead of finding or drawing a new picture for every slot; keep drawings as `<symbol>` + `<use>` or generate them with a small script so the page stays light. List every found picture (with its source and licence), every dealt photograph and every drawing that stands in for photography in your report.

Few images, used as inserts in the typography rather than as illustrations beside it: one photograph inside or behind the name (a 4:5 or 1:1 frame replacing a letter, or tucked between two words), then a short run of large full-width or half-width photographs further down. Square corners. No collage of small thumbnails.

**Floor (the inspector checks it):** at least four real pictures on the page, usually six to twelve; SVG drawings do not count. One moving picture where an honest clip exists: `node <skill>/scripts/assets.mjs --video "<query>"`, used as a muted loop with a poster frame. Whatever this direction says about pictures, it is carried out with real ones.

Photographs dealt for this build, from the "Architecture" set (structure, lines, bridges, facades and building interiors)
Order of preference for imagery: (1) the project's own photographs and product shots; (2) images you generate, if an image tool is
available; (3) real pictures of the subject's world found in the open collections (assets.mjs, downloaded and credited on the page);
(4) drawings of the subject in code; (5) these. They are real photographs (Unsplash licence, served by picsum.photos) of places, light and
texture. They are atmosphere, never a stand-in for a specific product, dish, person or interface. List the ones you use in your report so
they can be replaced.
- `https://picsum.photos/id/946/1600/1000` — Yellow brick house front with a dark green door and window · mid tone · ochre yellow, dark green, charcoal · native landscape · photo: Padurariu Alexandru
- `https://picsum.photos/id/870/1600/1000` — White lighthouse with its lamp lit against a deep blue starry sky · mid tone · deep blue, white, warm orange · calm area: right · native portrait · photo: Joshua Hibbert
- `https://picsum.photos/id/693/1600/1000` — Red suspension bridge tower rising from fog above rugged cliffs · mid tone · rust red, grey, dark teal · calm area: left · native landscape · photo: Rob Bye
- `https://picsum.photos/id/855/1600/1000` — Small figure walking past a huge bright yellow wall · light tone · bright yellow, black · calm area: left · native landscape · photo: Rodion Kutsaev
- `https://picsum.photos/id/508/1600/1000` — Tall pointed vaults and pale columns of a church interior · light tone · cream, warm grey, soft orange · native portrait · photo: Jeff Sheldon
- `https://picsum.photos/id/620/1600/1000` — White arched bridge spanning grey water under a pale sky · light tone · white, pale grey, charcoal · black-and-white · calm area: bottom · native landscape · photo: Matthew Wiebe
- `https://picsum.photos/id/954/1600/1000` — Narrow opening in a white wall revealing a white staircase · light tone · off-white, pale beige · calm area: left · native landscape · photo: Todd Quackenbush
- `https://picsum.photos/id/887/1600/1000` — White apartment block facade with repeating balconies and windows · light tone · white, pale grey, soft red · native landscape · photo: Roman Kraft
The last two path numbers are width and height: request the exact crop you render (`/1200/1500` for a 4:5 portrait, `/2400/1350` for a hero) and
add `?grayscale` to desaturate. Use three to six of them, not all eight. Always set `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).
Other sets that fit this brief: city-day, fog-and-quiet, coast, transport — `node draw.mjs --photos <set>` prints one in full; `--photos list` shows all sets. Taking photographs from another set is your call and is not a redraw; keep them to one light and one treatment.

## 6. Hero — Stacked name, two inks
One saturated flat field covers the whole 1440×900 viewport and there is no image. The name is broken into two lines and set flush left from a 40px margin at clamp(110px, 15vw, 230px), heavy weight, tracking -0.04em, line-height 0.82 so the lines almost touch. The block starts 14% down and fills the top 58% of the screen; the longer line reaches at least column 11. Line one is set in the light ink and line two in the dark ink, so the break reads as a change of voice: split a two-word name between the lines, or break one long name with a hyphen at a syllable. The top edge carries only small text at 15px, 24px in: a monogram top-left, and two or three text links plus the single action as an underlined link top-right. The supporting sentence, 18px in the light ink and max 30ch, is right-aligned in the bottom-right corner on columns 9–12, its last line 40px above the bottom edge. The bottom-left corner stays empty. The next section begins as a different flat field exactly at the fold.

On a phone: The field fills 100svh. The name keeps its two lines and two inks at 21vw, flush left at a 16px margin, starting 18% down; a long name hyphenates rather than dropping below 18vw. The supporting sentence moves to the bottom-left at 16px across the full width, with the action as an underlined link beneath it, 24px above the bottom edge. The top-right links reduce to one word.
Headline: The name on exactly two lines, one per ink, each line up to about 8 characters at 15vw on desktop and 21vw on a phone.

Adjusted for this page:
- Its action is a text link: the primary action on the first screen is a real button (filled or solid-bordered, 44px or taller), placed where the blueprint puts the link. A second action may stay a link.
- Its vw sizes assume a face of normal width: with this condensed display face, size the words to fill the measure the blueprint gives them instead of copying the vw value.

## 7. Sections, in order
Each is a composition to rebuild with this project's content. Keep the geometry; change the subject. Re-order or drop a
section when the argument of the page needs it (see references/copy.md), never to fall back to a card grid.

### 1. how-it-works — Photographs down a diagonal (stack)
Three stages, three photographs of different sizes placed along a falling diagonal on the 12-column grid. Stage one: a 3:4 portrait in columns 1–4. Stage two: a 1:1 square in columns 6–8, its top edge 220px lower than the first photograph's top. Stage three: a 16:10 landscape in columns 8–12, starting 180px below the bottom of the second. Each stage's text sits in the gap the stagger leaves: a paragraph of up to 36ch at 17px, top-aligned with its photograph and placed in the columns to its right (to its left for the third). Each paragraph opens with a bold run-in phrase that carries the order: 'On the first day', 'A week later', 'By the end'. Square corners; no arrows or connecting marks. The heading, two to four words at clamp(36px, 4vw, 64px) in a light weight, sits alone in columns 7–12 at the very top, level with the first photograph's top edge.
On a phone: The diagonal becomes alternating widths: the first photograph at 100%, the second at 62% flush right, the third at 78% flush left. Each paragraph follows its photograph on that photograph's left edge at 16px. 56px between stages. The heading sits above at 30px.

Adjusted for this page:
- Its vw sizes assume a face of normal width: with this condensed display face, size the words to fill the measure the blueprint gives them instead of copying the vw value.

### 2. proof — Names running off the edges (band)
A full-bleed band in a flat colour, about 34vh tall, holding a single line of names that is cropped by both viewport edges. The names are set at 8vw in the display weight, `white-space: nowrap`, separated by a solid round dot one third of the cap height, and the line moves slowly to the left (a CSS `translateX` animation over 40 seconds on a duplicated track, paused under `prefers-reduced-motion`). The band has no heading. Its meaning comes from one sentence at 18px set directly below the band at the left margin on the page ground, stating plainly who these names are. Supplied logos may replace names if all are available as single-colour SVGs at 0.8em height; do not mix logos and set names in one line. The band butts against the sections above and below with no gap.
On a phone: The band is 22vh tall with names at 15vw, still cropped at both edges and still moving. The explaining sentence sits under it at 16px with 20px margins. Do not add a second line running the opposite way; one line is the idea.

Adjusted for this page:
- Its vw sizes assume a face of normal width: with this condensed display face, size the words to fill the measure the blueprint gives them instead of copying the vw value.

### 3. about — Side facts, wide paragraph (table)
Two rows share one vertical line at 34% of the viewport width. Row one: in a 160px column at the left margin, three label and value pairs stack with 20px between them, each a label in the soft ink with its value beneath in full ink, all at 13px (founded, based in, team size). From the 34% line a five-line paragraph at clamp(20px, 1.7vw, 26px), leading 1.35, runs to 90% of the width. Row two starts 120px lower and repeats the logic for the record of the practice: one plain word at 13px at the far left (awards, press, clients), then from the 34% line two list columns, each 260px wide with a 64px gutter, at 13px with 10px between lines: name at the left, year at the right in the soft ink. No heading; the paragraph opens the section. Each list comfortably holds 6–12 lines. No photographs are needed.
On a phone: Everything aligns to the left margin. The paragraph comes first at 19px. The three label and value pairs follow as a two-column grid at 14px. The two record lists stack with 40px between them, each opened by its plain word in full ink.

Adjusted for this page:
- Its vw sizes assume a face of normal width: with this condensed display face, size the words to fill the measure the blueprint gives them instead of copying the vw value.

## 8. Motion — Masked headline
On load, each line of the headline rises from behind its own baseline, about 900ms with a strong ease-out, the second line 110ms after the first; the supporting sentence and the action then fade up together. Nothing else on the page performs. Because headlines are two lines at most, you author the line breaks and wrap each line yourself. Recipe: 'Masked line reveal' in references/motion.md.
This is the signature move, the one loud moment. Around it the page still needs the rest of the motion layer (SKILL.md step 9): an entrance for the parts of every section, feedback on every control, and one moving picture. The inspector fails a page that barely moves. Recipes: references/motion.md.

## 9. Where the richness comes from
Scale. The size of the name against the smallness of everything else is the entire visual event, so protect both ends: do not shrink the name to make room, and do not let body text creep above 20px.

## 10. How this direction goes wrong
A long name set small is just a logo. If the name has more than about 12 characters, stack it on two lines or crop it with the viewport edge; never drop below 12vw. Do not add a second big headline under the name. Do not decorate the letters.

## 11. Real references
Studied sites that work this way. Take the principle, never the specifics: no names, copy, images or signature assets of theirs.
- **NOTHIN’** (Awwwards Site of the Day, studied score 7.4) `aww-nothin`
  Idea: The studio's name set as a wordmark so large it is the whole hero, repeated in inverted colours as the footer, so 'nothing' is literally the only content on screen.
  Hero: The captured hero frame is a black preloader wipe; this describes the loaded state. White field. A custom heavy geometric wordmark in black spans the full width between 1% margins, vertically centred, about 30% of the viewport tall, its apostrophe hanging at the top-right. Top-left: a two-line statement at about 1.6vw with a small black pill button under it. Top-right: a tiny menu label with a four-dot icon. Along the bottom edge: a one-line studio descriptor at left, two social links and a language chip at right. Everything else is empty white, with no image and no colour.
  Worth taking: Make the hero nothing but the name: a wordmark scaled to the full viewport width on a blank field, with only a two-line statement and one small button in a corner.
- **Produx Design** (Awwwards Site of the Day, studied score 7.4) `aww-produx-design`
  Idea: The wordmark is the hero, and the showreel image assembles itself from scattered square fragments as you scroll.
  Hero: Near-black field with 80px side margins. The wordmark, in a wide, light-weight uppercase sans with a slashed O, runs margin to margin (about 89% of the width) with a cap height near 20% of the viewport, starting 9% from the top. A large empty gap follows. In the lower half a two-line statement at 5.1vw sits flush left; opposite it, bottom-aligned to the statement and flush to the right margin, is a three-line paragraph in small monospace about a quarter of the width. No nav bar, button or image in the first viewport; the bottom quarter is empty.
  Worth taking: Run the wordmark margin to margin in a light weight rather than a heavy one; thin strokes at huge size read as assured instead of loud.
- **ERA Residence** (Awwwards Site of the Day, studied score 7.6) `aww-era-residence`
  Idea: One continuous 3D render of the estate that the scroll flies through, titled like a perfume label with condensed didone capitals and an overlapping script signature.
  Hero: The captured first viewport is an intro curtain: a deep aubergine field with a hairline frame inset 22px and chamfered corners. At centre, a two-line title in tall condensed didone caps at about 6vw, with a thin script place-name overlapping its lower edge at an upward angle. On the same line, two wide-letterspaced caps words sit a third of the way in from each side. A ghost script word, barely lighter than the field, spans the full width behind. Flower mark top-centre; a 90px vertical hairline and two lines of tiny extended caps bottom-centre. It opens onto a full-bleed render with the same lockup at 12vw across the sky.
  Worth taking: Overlap a thin script word across the bottom edge of condensed didone capitals, angled upward, like a signature on a label.
Full notes on any of them: `node draw.mjs --site <id>`.

## Always
Headlines two lines or fewer at every width. No eyebrow labels, no monospace, no 01/02/03, no thin rules, no gradients, no shadows at rest,
no cream-and-terracotta, no violet. `inspect.mjs` measures all of it.

Saved to D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/design_lab/.taste-skill/direction.json · reprint with `node draw.mjs --show`
