# UNBROKEN with Dr. G — coming-soon site

Static landing page for the YouTube series, live at https://www.brokenwithdrg.com. Vercel deploys every push to `main` to production, so a push is a release.

## Workflow

1. Edit `src/template.html`. Never hand-edit `public/index.html`; it is generated.
2. Run `python3 src/build.py` to regenerate `public/`.
3. Check the page at 390px and 1440px wide (no horizontal scroll, no console errors).
4. Commit `src/` and `public/` together and push to `main`.

## Rules

- Follow the brand rules in README.md: ink `#0B0B0B` and bone `#F1ECE3`, one colour at a time (red is reserved for the recording light and the YouTube logo); Archivo only (Permanent Marker is used solely for the scrawl on the tape); logos from `src/brand/` used unmodified.
- Reuse the CSS tokens on `:root` and existing classes (`.display`, `.label`, `.tag-btn`) instead of new one-off styles.
- Keep motion behind `prefers-reduced-motion`.
- Don't invent guests, injuries, dates or partners. The intake charts are labelled as examples.
- Launch settings (`CHANNEL_URL`, `PREMIERE`) live at the top of the page script.

## Private partner page (/partners)

- The repo is public, so the partner deck is never committed in plain text. `src/partners.html` (the editable source) is gitignored; the committed copies are `src/partners.html.enc` and the encrypted `public/partners.html`, which asks for the password and decrypts in the browser.
- To edit or rebuild it you need the password: `PARTNER_PASSWORD=… python3 src/build.py`. Without `src/partners.html` on disk, the build decrypts the source from `src/partners.html.enc` (the build doesn't write the source back to disk). Without the variable, the build skips the partner page and leaves `public/partners.html` as it is.
- Changing the password: build once with the new `PARTNER_PASSWORD` while `src/partners.html` exists, and commit both encrypted files.
- The gate trims and lowercases what people type (phones capitalise the first letter), and the build does the same to `PARTNER_PASSWORD`, so passwords are effectively case-insensitive.
- Never commit `src/partners.html` or put the password in the repo.
- The partner page is the one exception to the red rule: it uses the deck's accent red (`--red`, `--red-hi`) for eyebrows, numbers, prices and the Founding Partners band, to match the partner deck. Logos stay unmodified.
