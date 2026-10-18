# BROKEN with Dr. G — coming-soon site

Static landing page for the YouTube series, live at https://www.brokenwithdrg.com. Vercel deploys every push to `main` to production, so a push is a release.

## Workflow

1. Edit `src/template.html`. Never hand-edit `public/index.html`; it is generated.
2. Run `python3 src/build.py` to regenerate `public/`.
3. Check the page at 390px and 1440px wide (no horizontal scroll, no console errors).
4. Commit `src/` and `public/` together and push to `main`.

## Rules

- Follow the brand rules in README.md: ink `#0B0B0B` and bone `#F1ECE3`, one colour at a time (red is reserved for the recording light and the YouTube logo); Archivo only; logos from `src/brand/` used unmodified.
- Reuse the CSS tokens on `:root` and existing classes (`.display`, `.label`, `.tag-btn`) instead of new one-off styles.
- Keep motion behind `prefers-reduced-motion`.
- Don't invent guests, injuries, dates or partners. The intake charts are labelled as examples.
- Launch settings (`CHANNEL_URL`, `PREMIERE`) live at the top of the page script.
