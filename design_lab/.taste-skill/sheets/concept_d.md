# DIRECTION SHEET — The quiet instrument
seed 191553536 · drawn 2026-10-14 · sector finance · tone quiet
Brief: Vietnamese house price estimator: enter a house's details, get an estimated price in ty dong from a trained model, stated as an estimate

| | |
| --- | --- |
| Direction | The quiet instrument |
| Hero | Control that reads the page |
| Type | Archivo |
| Colour | Navy on white |
| Sections | how-it-works (Pinned fragment, changing state) → proof (One quiet logo row) → about (Founder's letter) |
| Motion | Masked headline |
| Photographs | the "Sky and space" set, as atmosphere |

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
Radical understatement. Where every competitor shouts, this page almost whispers: a headline barely larger than body text, a narrow column, small exact demonstrations, and a great deal of untouched space. The restraint is the claim. It says the thing is simple, finished and sure of itself. This only works when it is carried through completely; one loud element breaks it. In the study, a tool for simple lists sold itself with a 27px headline and 12–14px copy and was one of the most confident pages in the set.

Before anything else, write one sentence in your notes: "On this page, <the subject's own material> becomes <the device>."
Fill the first blank from your inventory of what only this client has (its name and what it means, its street, its numbers, its
constraint), then put the nearest competitor in the sentence: if it still works, the idea is the category's, not the client's.
Then name the one live thing the visitor can do on the page (SKILL.md step 4).

## 2. Composition
A single column 440–560px wide, placed left of centre (starting at about 22% of the viewport width) or dead centre, running the whole page. The headline is the one large thing on the first screen: two lines at display size (5–7vw), medium weight, starting on the column's left edge and allowed to run wider than the column. The supporting paragraph follows at body size (17–19px) in the full ink. One small primary button and one text link. Below, each point is a short paragraph followed by a compact demonstration or image no wider than the column. Sections are separated only by space (96–140px). Nothing spans the full width until the footer, which is a single quiet line. The first screen is mostly empty and that emptiness is composed: the column's top edge sits at about 30% of the viewport height.

## 3. Type — Archivo
A sturdy grotesque kept at regular weight even at 88px, so the page reads as composed rather than loud. Suits finance, infrastructure and research pages that need to look sober and current.
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600&display=swap" rel="stylesheet">
```
- Display: **Archivo** — weight 400 · tracking -0.02em · leading 1.0 · sentence case; never bold, inactive items fade to grey
- Text: **Archivo** — 400 for body, 600 for buttons and short emphasis · leading 1.5 · tracking 0
```css
:root {
  --step-small: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --step-body: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
  --step-lead: clamp(1.25rem, 1.1rem + 0.7vw, 1.625rem);
  --step-head: clamp(2rem, 1.3rem + 3.2vw, 4rem);
}
```
One family, two weights. A display size for the headline (5–7vw), one heading size for section titles (about 32–40px), body at 17–19px, a small size for captions (14–15px). Leading 1.5 for text. Letter-spacing near zero. The typeface must be handsome at small sizes.
The direction decides sizes and how many of them; the type system decides how this face is set. Where the two give different tracking or leading, use the values of the type system: they are tuned to this face.
The display size itself comes from the hero blueprint below.

## 4. Colour — Navy on white
```css
:root {
  --bg: #ffffff;
  --surface: #f4f4f2;
  --ink: #1f2b4d;
  --muted: #6a7186;
  --accent: #f7941d;
  --accent-ink: #1f2b4d;
  --field-1: #05070a;  --field-1-ink: #ffffff;
  --field-2: #e3e1dc;  --field-2-ink: #1f2b4d;
}
```
Pure white pages with navy type sit between full-bleed photographs, opening on near-black and closing on a warm grey footer. Tangerine is one small tab or button, never larger than a thumbnail.
Paper and two inks (full and soft). One accent used on exactly one element per screen.

## 5. Imagery
**This subject is software and there are no screenshots, so its pictures are its own interface.** Wherever this sheet says photograph, image or object, build a believable fragment of the product in HTML at real size (real labels, numbers that add up, one item hovered or selected), put the attribute `data-ui` on its root, and crop or scale it the way the blueprint treats a photograph: a full-bleed close crop, a tile, the fixed half of a split. Where a fragment makes no sense, use a flat colour field with type on it. Never a fake dashboard of grey bars, never a device frame. If the product works on something physical (ships, plants, buildings, a city), one real picture of that world can carry a section: find it with `node D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/.claude/skills/design-taste-frontend/scripts/assets.mjs "<that world>"`, download it with `--get`, credit it on the page, and never let it pass for the product or its customers.

Precise rather than loud: cropped interface details at true size, and real photographs of the customer's world held to the column width, each doing one job. One short looping clip can sit at column width too. Never a large stock hero image.

**Floor (the inspector checks it):** at least four real pictures on the page, usually six to twelve; SVG drawings do not count. One moving picture where an honest clip exists: `node <skill>/scripts/assets.mjs --video "<query>"`, used as a muted loop with a poster frame. Whatever this direction says about pictures, it is carried out with real ones.

Optional atmosphere, two at most, from the "Sky and space" set (skies, clouds, stars and night skies). The page does not need them.
Order of preference for imagery: (1) the project's own photographs and product shots; (2) images you generate, if an image tool is
available; (3) real pictures of the subject's world found in the open collections (assets.mjs, downloaded and credited on the page);
(4) drawings of the subject in code; (5) these. They are real photographs (Unsplash licence, served by picsum.photos) of places, light and
texture. They are atmosphere, never a stand-in for a specific product, dish, person or interface. List the ones you use in your report so
they can be replaced.
- `https://picsum.photos/id/505/1600/1000` — Tiny silhouetted figure on a dark ridge under a blue and orange twilight sky · dark tone · deep blue, orange, black · calm area: top · native landscape · photo: lee Scott
- `https://picsum.photos/id/869/1600/1000` — Starry night sky above a mountain glowing warm at its peak · dark tone · navy, deep blue, amber · calm area: top · native landscape · photo: Caleb Ralston
- `https://picsum.photos/id/38/1600/1000` — White cumulus cloud rising against a dark teal sky · mid tone · dark teal, white · calm area: top · native landscape · photo: Allyson Souza
- `https://picsum.photos/id/765/1600/1000` — Night sky fading to an orange glow along a dark horizon · dark tone · midnight blue, burnt orange, black · calm area: top · native landscape · photo: Grant McIver
The last two path numbers are width and height: request the exact crop you render (`/1200/1500` for a 4:5 portrait, `/2400/1350` for a hero) and
add `?grayscale` to desaturate. Use at most two. Always set `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).
Other sets that fit this brief: architecture, fog-and-quiet, water — `node draw.mjs --photos <set>` prints one in full; `--photos list` shows all sets. Taking photographs from another set is your call and is not a redraw; keep them to one light and one treatment.

## 6. Hero — Control that reads the page
A near-black or deep neutral ground split into two halves by tone alone: the right half is one step lighter than the left, and they meet at a clean vertical edge at 50%. Left half: a small logo mark top-left at a 40px margin, then two-thirds of empty ground, then everything else anchored bottom-left, 40px from the edges: a one-line headline at clamp(26px, 2.1vw, 32px) in medium weight, one supporting sentence at 17px in the softer ink held to 44ch, and the single action as a light rectangular button. Right half: one fragment of the product, centred, about 450px square, built in HTML and working. It is the product's defining control (a loupe, a picker, a dial, a field) and it acts on the page itself: it reads the real background colour, the real headline size or the pointer position and prints that value in its own readout at 13px. Mark its root with data-ui so the product's own radii and borders apply inside it. There is no navigation bar; one text link sits top-right at 15px.

On a phone: The halves stack as two tones. The fragment comes first: 78vw square, centred in the lighter block, which is 58svh tall, still live and reading the page under the visitor's finger. The darker block below holds the headline at 6.4vw on up to two lines, the sentence at 16px and the button, left-aligned at 20px. The logo mark sits top-left over the first block.
Headline: One plain line at 26–32px naming what the tool is, up to about 32 characters, wrapping to two lines on a phone.

Adjusted for this page:
- It names colours (black): map them onto this palette's roles (ground `--bg`, panels `--surface` and the fields, text `--ink`/`--muted`, the accent `--accent` on the primary action only).
- It draws lines or borders: keep them only inside a table, a form or a `data-ui` fragment; elsewhere separate with space or a change of ground.

## 7. Sections, in order
Each is a composition to rebuild with this project's content. Keep the geometry; change the subject. Re-order or drop a
section when the argument of the page needs it (see references/copy.md), never to fall back to a card grid.

### 1. how-it-works — Pinned fragment, changing state (pinned)
Two columns. Right, columns 7–12: a stage that is position: sticky; top: 14vh, holding one fragment of the real interface at true size on a single flat stage colour, about 520px square. Left, columns 1–5: three statements, each in its own block 80vh tall, so one is in view at a time. A statement is a two-line sentence at 28–32px that begins with its order word ('Paste a link.', 'Then pick the parts you want.', 'Share it when it looks right.') plus one supporting line at 16px. The statement nearest the viewport's centre is in full ink; the others sit at 30%. As each statement becomes active the fragment changes to the matching state: an empty field, a filled list with two rows selected, a finished result with its confirmation. Build the states in HTML and switch a class; do not swap screenshots. The heading, two to four words at 24–28px, sits above the first statement.
On a phone: The stage is sticky at the top, 46svh tall, the fragment fitted by cropping to its active region, not by shrinking its text. Statements scroll beneath it in blocks 60svh tall at 22px. The stage releases after the third statement.

Adjusted for this page:
- It fades text: anything a visitor reads, inactive items of a list included, is `--ink` or `--muted` at full strength (contrast 4.5:1 or more). The active item is told apart by `--ink` against `--muted`, weight or the accent, not by fading the rest.

### 2. proof — One quiet logo row (strip)
Only for real logos supplied by the project; if none are supplied, set the names in the text face at 22px in the same row and never draw stand-ins. The row reads as a sentence: it opens at the left margin with two to four plain words at 18px (the phrase that introduces the names), vertically centred on the logos, and five to seven logos follow on the same line, spread to the right margin with `justify-content: space-between`. Every logo is normalised to one optical height (28–32px for wordmarks, 36px for compact marks) and one colour, the page ink, using single-colour SVGs with `fill: currentColor`. The band is tall and almost empty: 120–150px of ground above and below the row, no box, no background change and no separate heading. Logos stay still; nothing scrolls or fades at the edges.
On a phone: The opening words sit alone on the first line at 17px. Logos follow in a grid of two per row, each 26px tall and left-aligned in its cell, with 36px between rows. Show six at most; there is no sideways scrolling.

### 3. about — Founder's letter (stack)
A letter in a centred column 520px wide with at least 160px of empty ground above and below. At the column's top-left, a round portrait 44px across. 28px below it, four or five short paragraphs at 16–17px with leading 1.55, each two to four lines and separated by one blank line, written in the first person. No heading. The sign-off is the writer's name at 22px in the text face's italic, with the role at 14px in the soft ink beneath it. One phrase in the letter may carry a flat marker-colour background. Variant for a page built as an object: the letter sits on a filled paper-colour sheet 640px wide with 60px padding on a contrasting ground, square corners, its bottom edge cut into small scallops with `clip-path`, and below a row of 5px round dots a tear-off strip 72px tall that carries the email address.
On a phone: The column takes the full width with 24px margins; text at 16px, portrait 40px. In the sheet variant the sheet spans edge to edge with 24px padding and keeps its shaped bottom edge; the tear-off strip stacks the email above a full-width button.

Adjusted for this page:
- It names a kind of typeface: use the dealt faces (display Archivo, text Archivo) and their settings; capitals only where the type system sets them.

## 8. Motion — Masked headline
On load, each line of the headline rises from behind its own baseline, about 900ms with a strong ease-out, the second line 110ms after the first; the supporting sentence and the action then fade up together. Nothing else on the page performs. Because headlines are two lines at most, you author the line breaks and wrap each line yourself. Recipe: 'Masked line reveal' in references/motion.md.
This is the signature move, the one loud moment. Around it the page still needs the rest of the motion layer (SKILL.md step 9): an entrance for the parts of every section, feedback on every control, and one moving picture. The inspector fails a page that barely moves. Recipes: references/motion.md.

## 9. Where the richness comes from
Precision. With so little on the page, alignment, spacing and the exact size relationships are the design. Every element shares the column's left edge.

## 10. How this direction goes wrong
This is the one direction where a small headline is right; the inspector will not object, but do not mix it with a large display line. Emptiness must look decided: keep the column edges exact and the vertical rhythm even. Not suitable when the subject needs emotion or photography to sell. Quiet is not thin: the column must still deliver every piece of content the brief asks for, in full, at 16px or more in the full ink. In blind tests the quiet version lost every time it was quiet everywhere: a small headline beside an empty panel read as unfinished. Quiet means few things, not small things: the headline and the demonstration are large, and every screen holds content.

## 11. Real references
Studied sites that work this way. Take the principle, never the specifics: no names, copy, images or signature assets of theirs.
- **Gil Huybrecht** (Awwwards Site of the Day, studied score 7.6) `aww-gil-huybrecht`
  Idea: A portfolio as a contact sheet: every project is a numbered run of miniature page screenshots on black, and all text is set at one small size.
  Hero: Black field on a seven-column grid with 14px margins. The top band is plain white text at one size, about 16px: name in column one, availability in column two, a services list from column three, a longer awards list from column five, then 'Profile' and 'Email me' at the right. List items are indented one step under their label. Below the lists roughly 300px of black is left empty. At mid-height the thumbnail grid begins: one small website screenshot per column, about 190px wide, each topped by a number at its right corner, with the project name over the first of each run. Two tiny toggle chips sit in the bottom corners.
  Worth taking: Set every piece of text on the page at one size and weight and build hierarchy only from column position and a one-step indent under labels.
- **Plastic** (One Page Love, studied score 7.1) `opl-plastic`
  Idea: A plain, quiet app page given one physical object: a photographed vinyl record cropped by the top-right corner of the viewport.
  Hero: Pale grey page with no navigation, only a bold wordmark with a small orange-red caps descriptor beneath it at top left (80px margin). A photographed black vinyl record with an orange-red label is cropped by the top-right corner, showing a quarter disc about 360px wide and tall, with an orange wire stand poking out below it. The headline is centred slightly above the middle in two lines at 74px (5.2vw), about 37% of the viewport wide, followed by a two-line 17px sentence and two black store badges side by side. Lower down, an award mark and a laurel-framed rating sit centred; the bottom fifth is empty.
  Worth taking: Crop one photographed physical object by a viewport corner so the hero has a subject without a centred mockup.
- **Tara** (One Page Love, studied score 7.2) `opl-tara`
  Idea: Two pastel circles, mint for saving and pink for spending, stand for the app's two accounts and recur as icon, inline dot, section colour and card gradient.
  Hero: Off-white field with no navigation, only a small bold wordmark top-left. The left column is vertically centred and starts about 8% in: a two-line headline in a wide heavy grotesk at roughly 6vw with tight leading, a grey one-line subhead beneath, then a pill-shaped email field about 400px wide with a black pill button nested inside its right end. The right half holds a 3D pair floating on the page colour: a mint-to-pink gradient bank card tilted about 30 degrees, overlapping a perspective-tilted phone showing a balance screen. Two small award badges are stacked on the right edge. Roughly half the viewport is empty.
  Worth taking: Assign each product concept a colour and a shape early (two pastel circles), then reuse it as bullet, inline punctuation dot and full section background.
Full notes on any of them: `node draw.mjs --site <id>`.

## Always
Headlines two lines or fewer at every width. No eyebrow labels, no monospace, no 01/02/03, no thin rules, no gradients, no shadows at rest,
no cream-and-terracotta, no violet. `inspect.mjs` measures all of it.

Saved to D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/design_lab/.taste-skill/direction.json · reprint with `node draw.mjs --show`
