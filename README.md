# BROKEN with Dr. G — brokenwithdrg.com

Coming-soon landing page for the YouTube series. Static HTML, deployed by Vercel on every push to `main`.

- `src/template.html` — the page (edit this)
- `src/brand/` — logo SVGs and web icons from the brand kit
- `src/build.py` — run `python3 src/build.py` to regenerate `public/`
- `public/` — what Vercel serves

Launch settings live at the top of the page script in `src/template.html`: `CHANNEL_URL` (YouTube channel) and `PREMIERE` (date, turns on the countdown).
