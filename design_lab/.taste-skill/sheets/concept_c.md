# DIRECTION SHEET — The product performs
seed 1811807192 · drawn 2026-10-14 · sector finance · tone bold
Brief: Vietnamese house price estimator: enter a house's details, get an estimated price in ty dong from a trained model, stated as an estimate

| | |
| --- | --- |
| Direction | The product performs |
| Hero | Fragment on a shaped stage |
| Type | Switzer |
| Colour | Sheet and biro |
| Sections | how-it-works (Call and response column) → proof (Large marks on tiles) → about (Founder's letter) |
| Motion | Shutter image |
| Photographs | the "Water" set, as atmosphere |

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
Software is most convincing when it is doing its job in front of you. Instead of describing features, put small, true, working fragments of the product on the page: the actual control, with real content, responding to the pointer. A colour picker's loupe reads the page's own background and prints its value. A list tool lets you tick an item right there. A type-scale plugin sets the page's own headings. Find the one interaction that is the product and make the hero that interaction; then show each further capability as another fragment at real size. No dashboard collage, no browser frame, no screenshots shrunk until unreadable.

Before anything else, write one sentence in your notes: "On this page, <the subject's own material> becomes <the device>."
Fill the first blank from your inventory of what only this client has (its name and what it means, its street, its numbers, its
constraint), then put the nearest competitor in the sentence: if it still works, the idea is the category's, not the client's.
Then name the one live thing the visitor can do on the page (SKILL.md step 4).

## 2. Composition
Hero: a short plain headline (4–6vw, left-aligned, upper-left third) and one sentence; the rest of the first screen is the main fragment at actual interface size, sitting directly on the page or on one flat stage colour, large enough to read every label. The fragment is built in HTML and works. Below, capabilities are a single-column sequence, each a row of two parts on a 5/7 split: a two-line statement on one side and the relevant fragment on the other, with the fragments varying in size and shape so the column never becomes a zigzag of equal blocks. Fragments are cropped pieces of interface (a menu, a row, a control, a panel edge), not whole windows. One section pins a fragment while three short statements change it.

## 3. Type — Switzer
One neo-grotesk doing everything: semibold headings pulled tight, small regular text, no capitals and no second voice. Suits software, hardware and studio pages that want to look exact and unshowy.
```html
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>
<link href="https://api.fontshare.com/v2/css?f[]=switzer@400,500,600&display=swap" rel="stylesheet">
```
- Display: **Switzer** — weight 600 · tracking -0.04em · leading 0.95 · sentence case; charcoal rather than pure black
- Text: **Switzer** — 400 for body, 500 for emphasis · leading 1.5 · tracking -0.005em
```css
:root {
  --step-small: clamp(0.8125rem, 0.79rem + 0.1vw, 0.875rem);
  --step-body: clamp(1.0625rem, 1rem + 0.25vw, 1.1875rem);
  --step-lead: clamp(1.25rem, 1.1rem + 0.7vw, 1.625rem);
  --step-head: clamp(2rem, 1.3rem + 3.2vw, 4rem);
}
```
The marketing type matches the product's interface type so the fragments and the page feel like one thing. Headline modest; interface text at its true size (13–15px) inside fragments.
The direction decides sizes and how many of them; the type system decides how this face is set. Where the two give different tracking or leading, use the values of the type system: they are tuned to this face.
The display size itself comes from the hero blueprint below.

## 4. Colour — Sheet and biro
```css
:root {
  --bg: #ffffff;
  --surface: #f4f4f4;
  --ink: #111111;
  --muted: #6b6b6b;
  --accent: #1a4be0;
  --accent-ink: #ffffff;
  --field-1: #111111;  --field-1-ink: #ffffff;
}
```
White holds the whole page with black type, one grey for secondary lines and a pale grey step for tiles and inputs; the footer may invert to black. Blue is the colour of text links and the one button, and nothing else is tinted.
Neutral ground. The product's own interface colours provide the colour. At most one flat stage colour behind fragments.

## 5. Imagery
**This subject is software and there are no screenshots, so its pictures are its own interface.** Wherever this sheet says photograph, image or object, build a believable fragment of the product in HTML at real size (real labels, numbers that add up, one item hovered or selected), put the attribute `data-ui` on its root, and crop or scale it the way the blueprint treats a photograph: a full-bleed close crop, a tile, the fixed half of a split. Where a fragment makes no sense, use a flat colour field with type on it. Never a fake dashboard of grey bars, never a device frame. If the product works on something physical (ships, plants, buildings, a city), one real picture of that world can carry a section: find it with `node D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/.claude/skills/design-taste-frontend/scripts/assets.mjs "<that world>"`, download it with `--get`, credit it on the page, and never let it pass for the product or its customers.

The interface fragments are the main imagery: build them carefully with real labels, real numbers and sensible states (one hovered, one selected). Around them, two or three real pictures of the customer's world (found with scripts/assets.mjs), never stock of people at laptops.

**Floor (the inspector checks it):** at least four real pictures on the page, usually six to twelve; SVG drawings do not count. One moving picture where an honest clip exists: `node <skill>/scripts/assets.mjs --video "<query>"`, used as a muted loop with a poster frame. Whatever this direction says about pictures, it is carried out with real ones.

Optional atmosphere, two at most, from the "Water" set (lakes, rivers, waterfalls and water surfaces). The page does not need them.
Order of preference for imagery: (1) the project's own photographs and product shots; (2) images you generate, if an image tool is
available; (3) real pictures of the subject's world found in the open collections (assets.mjs, downloaded and credited on the page);
(4) drawings of the subject in code; (5) these. They are real photographs (Unsplash licence, served by picsum.photos) of places, light and
texture. They are atmosphere, never a stand-in for a specific product, dish, person or interface. List the ones you use in your report so
they can be replaced.
- `https://picsum.photos/id/1038/1600/1000` — Small red boat on a wide expanse of dark blue rippling sea · dark tone · deep blue, slate, red · calm area: bottom · native portrait · photo: Marcelo Quinan
- `https://picsum.photos/id/469/1600/1000` — Two people paddling a canoe across a misty green lake · mid tone · emerald green, pale grey, teal · calm area: bottom · native landscape · photo: Matthew Clark
- `https://picsum.photos/id/124/1600/1000` — Small red boat floating on clear turquoise water, seen from above · mid tone · turquoise, teal, red · calm area: right · native landscape · photo: Anton Sulsky
- `https://picsum.photos/id/293/1600/1000` — Silhouetted pier on a hazy blue lake below faint mountains · mid tone · pale blue, navy · calm area: left · native landscape · photo: Paul E. Harrer
The last two path numbers are width and height: request the exact crop you render (`/1200/1500` for a 4:5 portrait, `/2400/1350` for a hero) and
add `?grayscale` to desaturate. Use at most two. Always set `width`, `height`, `alt` and `loading="lazy"` (not on the hero image).
Other sets that fit this brief: architecture, fog-and-quiet, sky-and-space — `node draw.mjs --photos <set>` prints one in full; `--photos list` shows all sets. Taking photographs from another set is your call and is not a redraw; keep them to one light and one treatment.

## 6. Hero — Fragment on a shaped stage
A neutral ground. The headline occupies the upper-left third: two lines at clamp(52px, 5.2vw, 80px), medium weight, flush left on columns 1–6 at a 40px margin, starting 150px down. One supporting sentence at 18px, max 40ch, follows, then the single action as a small rectangular button. The rest of the screen belongs to one flat stage in a saturated colour: it spans columns 5–12, begins 42% down, and bleeds off the right and bottom edges. Its top-left corner is cut with the product's own shape using `clip-path` (a notch, a chamfer or a tab two columns wide), the only decoration on the page. On the stage, 56px in from its left and top edges, sits the main fragment of the interface at true size with labels at 13–15px, built in HTML and working: one panel or control about 620px wide, cropped by the bottom edge, never a whole window and never inside a browser or laptop frame. Mark its root with data-ui. Navigation is a plain row at 28px from the top: wordmark left and four text links right at 15px. Nothing overlaps the headline.

On a phone: The headline sits under the wordmark at 10vw on two lines, followed by the sentence at 16px and the button. The stage comes next at full width, bleeding off both sides and the bottom, its corner cut kept at 72px wide. The fragment sits 16px inside it at true size; if it is wider than the screen the right edge crops it rather than scaling it down.
Headline: A plain statement of what the product does in three to six words, two lines of up to about 16 characters each at 5.2vw.

## 7. Sections, in order
Each is a composition to rebuild with this project's content. Keep the geometry; change the subject. Re-order or drop a
section when the argument of the page needs it (see references/copy.md), never to fall back to a card grid.

### 1. how-it-works — Call and response column (list)
The sequence is shown as what you give and what comes back, in one narrow column 560px wide starting at column 4, or on the page's text axis. Three exchanges, 88px apart. Each opens with a sentence at 20px medium that begins with its order word ('First, install it.' 'Then ask for a chart.'). 16px under it, the call: the literal thing the user enters, in a filled panel one tone off the ground, radius 8px, padding 20px. For a developer tool that is real code in `<pre><code>` at 14px with a working copy button; otherwise it is the product's own input holding real typed text. Under the call, indented 56px, the response: a true-size fragment marked data-ui showing what the product returns. The third response is the finished result and breaks out of the column, 760px wide, running to column 12. The heading, two to four words at 28px, sits 56px above the first sentence.
On a phone: The column fills the width with 20px margins. Calls and responses stack without the indent; a 24px gap and a lighter panel tone set the response apart. Code panels scroll sideways inside themselves. The final result runs edge to edge at true size, cropped on the right if wider.

Adjusted for this page:
- It names its own corners: use the one radius of this page (square unless the direction says otherwise) and one button shape.

### 2. proof — Large marks on tiles (grid)
A board of filled tiles, four across and two or three rows deep, with 8px gaps, spanning the full content width. Each tile is about 3:2, one step lighter or darker than the page ground, with no border. A tile holds one supplied logo, shown far larger than a usual logo strip: about 72px tall, centred, in the page ink as a single-colour SVG. When no logo files exist, the tile holds the name instead, set at 28–32px bold, top-left with 24px padding; never draw a mark. One tile, twice the width of the others and placed first, is in the accent colour and carries the heading: two to four words at about 3vw, top-left. Tile corners follow the page's one radius, or the page's motif shape if it has one. Tiles sit still; there is no hover lift.
On a phone: Two tiles per row with 6px gaps, logos at 44px tall. The heading tile runs full width first, about 120px tall. Show eight tiles at most so the board stays under one and a half screens. Names set in type drop to 20px.

### 3. about — Founder's letter (stack)
A letter in a centred column 520px wide with at least 160px of empty ground above and below. At the column's top-left, a round portrait 44px across. 28px below it, four or five short paragraphs at 16–17px with leading 1.55, each two to four lines and separated by one blank line, written in the first person. No heading. The sign-off is the writer's name at 22px in the text face's italic, with the role at 14px in the soft ink beneath it. One phrase in the letter may carry a flat marker-colour background. Variant for a page built as an object: the letter sits on a filled paper-colour sheet 640px wide with 60px padding on a contrasting ground, square corners, its bottom edge cut into small scallops with `clip-path`, and below a row of 5px round dots a tear-off strip 72px tall that carries the email address.
On a phone: The column takes the full width with 24px margins; text at 16px, portrait 40px. In the sheet variant the sheet spans edge to edge with 24px padding and keeps its shaped bottom edge; the tear-off strip stacks the email above a full-width button.

Adjusted for this page:
- It names a kind of typeface: use the dealt faces (display Switzer, text Switzer) and their settings; capitals only where the type system sets them.

## 8. Motion — Shutter image
The one hero or showcase image opens from an edge with a clip-path over about 1.1 seconds while the picture inside settles from 1.12 scale to rest. Use it once, on the image that matters most; later images simply are there. Recipe: 'Image shutter' in references/motion.md.
This is the signature move, the one loud moment. Around it the page still needs the rest of the motion layer (SKILL.md step 9): an entrance for the parts of every section, feedback on every control, and one moving picture. The inspector fails a page that barely moves. Recipes: references/motion.md.

## 9. Where the richness comes from
Fidelity. A fragment with believable content and a real hover state is more interesting than any illustration. Spend the effort there.

## 10. How this direction goes wrong
A fake interface made of grey bars and circles is the worst outcome; if you cannot build a believable fragment, change direction. Mark each fragment's root element with the attribute data-ui: inside it the product's own conventions apply (1px control borders, small radii, a shadow on its open menu) and the inspector leaves them alone; outside it the house rules hold as usual. data-ui is for cropped fragments only, never for a page wrapper. Do not put the fragment in a browser or laptop frame.

## 11. Real references
Studied sites that work this way. Take the principle, never the specifics: no names, copy, images or signature assets of theirs.
- **Uni** (One Page Love, studied score 7.2) `opl-uni`
  Idea: The product lives in the laptop notch, so the page's navigation is a black notch and the hero is a laptop outline whose notch opens into the app.
  Hero: White page with the hero as a rounded-corner panel inset 24px on all sides, filled with a grainy pastel gradient (pink-peach centre, sky blue down the right edge, orange lower-left). A black pill 300×44px sits top-centre like a laptop notch, holding only the app icon; it is the entire nav. Centred below: a hand-scrawled caps eyebrow, a two-line 48px (3.3vw) headline, two white pill download buttons side by side, one line of tiny grey reassurance. The bottom 40% is a thick black outline of a laptop screen, 960px wide, cropped by the fold, its notch expanded into a dark input bar playing the demo.
  Worth taking: Shape the navigation like the product's own hardware habitat (here a black notch pill) so the nav itself demonstrates the product.
- **Dabbit** (One Page Love, studied score 7.8) `opl-dabbit`
  Idea: The colour picker demonstrates itself on the page: its loupe sits in the hero reading the site's own background hex, and every feature is shown as a real fragment of the app.
  Hero: Near-black viewport split exactly in half by a one-pixel vertical hairline. Left half: a small chrome four-petal logo top-left at a 40px margin, then two thirds of empty dark, then everything else anchored bottom-left: a one-line 30px medium-weight headline, three lines of grey 18px copy, a light pill button beside an outlined pill, and a tiny note. Right half: a 450px rounded square with a thin iridescent border, the app's loupe, empty except for a centre crosshair dot and a small chip reading the hex of the page's own background. Eight pastel dots and lozenges drift across the top-right like spilled swatches.
  Worth taking: Make the hero demo sample the page itself: the tool reports the site's own background value, proving the product without a screenshot.
- **Dragonfly Redux** (Awwwards Site of the Day, studied score 8.2) `aww-dragonfly-redux`
  Idea: A crypto fund presented as a terminal artefact: every picture is rendered in ASCII characters, framed by four letters of the name pinned to the viewport corners.
  Hero: Pure black viewport. A live canvas draws a dragonfly and foliage out of grey ASCII glyphs, running diagonally across the whole screen and fading toward the bottom. Dead centre, the fund's name in orange uppercase grotesk at about 11vw spans the middle 65% of the width on one line, overlapping the insect's body. A small dark-grey bar, 380px wide, is centred at the top holding a logo glyph, a five-dot orange progress indicator and a mono menu label. One white serif capital sits in each viewport corner (one mirrored), with tiny plus-shaped crop marks just inside them. No tagline and no button.
  Worth taking: Pin one letter of the brand in each viewport corner as a permanent frame, so even an empty black screen feels composed.
Full notes on any of them: `node draw.mjs --site <id>`.

## Always
Headlines two lines or fewer at every width. No eyebrow labels, no monospace, no 01/02/03, no thin rules, no gradients, no shadows at rest,
no cream-and-terracotta, no violet. `inspect.mjs` measures all of it.

Saved to D:/DangKhoa/Aiqs/AIQS-Real-Estate-Price-Prediction/design_lab/.taste-skill/direction.json · reprint with `node draw.mjs --show`
