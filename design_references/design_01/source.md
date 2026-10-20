# design_01 — source

| | |
|---|---|
| File | `C:\Users\dangkhoa\Downloads\ref\Screen Recording 2026-10-14 091300.mp4` |
| Type | Screen recording, 12.6 s, 1018×786, H.264 |
| SHA-256 (first 12) | `a11e7876f7c0` |
| Subject | "Puzzle", accounting software, shown as a design case-study presentation |
| URL | None visible; not known whether a live page exists |
| Captured here | 14 evenly spaced frames in `screenshots/`, extracted with headless Chrome (`../_tools/extract_frames.mjs`) |

## What the recording shows (observed)

- A bento board of seven dark rounded panels on a near-black ground:
  - a desktop landing page with a "For founders / For accountants" toggle, centred headline and testimonial card;
  - a phone screen with a 2×2 feature-icon grid and a mint "Get started" button;
  - a donut gauge reading "$1.2M ↑ Up 12%", animating between values;
  - a colour-swatch panel with printed hex values;
  - a pill bar (UI/UX, Brand Personality, Illustrations) whose active pill cycles;
  - a navigation bar with an open dropdown (Founders, Accountants, Testimonials, API);
  - a laptop mock-up of the landing page.
- The content of the large left panel changes as the pills cycle.
- A video-player progress bar appears in one frame (f12): the recording was taken from a playing video.

## Not observable

- Live page structure, CSS values, real font names, breakpoints, focus styles, hover timings.
- Any text smaller than about 7 capture px.

## How it was analysed

The Taste skill's analysis Steps 1–4 were applied to frames and pixel measurements (`taste/`), because its browser capture step needs a live URL. The user approved this substitution on 2026-10-14. No page was crawled.
