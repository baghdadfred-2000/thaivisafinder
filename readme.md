# Uncle Pong's Thailand Visa Finder

An independent, single-page web tool that weighs **all 18 legal Thailand long-stay visa routes** against a visitor's situation and returns Good / Better / Best recommendations with real 2026 costs, honest pros and cons, next steps, and a "where in Thailand you'd be happiest" location match.

- **Production domain:** https://thaivisafinder.com
- **Brand:** Uncle Pong's Thailand (sibling to https://thaiholidaybudget.com)
- **Operator:** Genext Information Systems
- **Visa data reviewed:** June 2026
- **Not legal advice** — informational/planning tool only.

---

## Files

```
Thailand Visa Finder/
├── index.html          ← the whole site (self-contained, deploy as-is)
├── robots.txt          ← upload to site root
├── sitemap.xml         ← upload to site root, submit in Search Console
├── README.md           ← this file
├── SEO-report.md       ← full SEO analysis, changes & Google action plan
└── images/
    ├── logo.png        ← circular Uncle Pong site logo / favicon
    ├── og-image.jpg    ← 1200×630 social/preview card (referenced by index.html)
    ├── pattaya.jpg     ← destination photos (also embedded in index.html)
    ├── chiang-mai.jpg
    ├── krabi.jpg
    └── phuket.jpg
```

## Deploy (any static host)

1. Upload the folder contents to your web root so the tool is served at `https://thaivisafinder.com/`.
2. Make sure `robots.txt`, `sitemap.xml`, and the `images/` folder sit at the root (the `og-image.jpg` social card and the `<meta property="og:image">` tag expect `https://thaivisafinder.com/images/og-image.jpg`).
3. That's it — there's no build step, framework, or server code. It's plain HTML/CSS/JS.

Works on Netlify, Cloudflare Pages, GitHub Pages, Vercel, S3+CloudFront, or classic shared hosting.

## Images: two copies on purpose

- The four destination photos are **embedded directly inside `index.html`** as data URIs, so the page is fully portable and shows photos even with nothing else uploaded.
- The same photos plus the OG card live in **`/images/`** as normal files. For production you may prefer to switch the location cards to external `<img src="/images/…">` references (smaller HTML, browser caching, better image SEO). See SEO-report.md.

## Known to-dos

- **Bangkok photo:** the supplied Bangkok image was a watermarked "PREVIEW" stock comp and was **not** used. Drop a licensed Bangkok photo into `/images/bangkok.jpg` and wire it in.
- **Cookie consent** is session-only in this build; persist the choice in a cookie/localStorage for production.
- **Legal/About/FAQ pages** are client-side views at the same URL. For best SEO, consider splitting them into real URLs (`/about`, `/faq`, etc.) — see SEO-report.md.

## How the recommendation engine works (quick version)

Two stages: (1) **hard eligibility gates** screen each visa for age, bank/income thresholds, work rights, marital/family status, etc.; (2) **weighted scoring** ranks the eligible routes by timeline, situation, priority and budget. Top three become Best/Strong/Worth-a-look; the next two are shown as "also considered." An affordability gate gives an honest "maybe not now" message to anyone who couldn't realistically fund the move, and nationality notes flag passports that need a visa arranged in advance.

All figures are mid-2026 estimates in ranges and must be re-verified against official Thai sources before anyone acts — immigration rules change frequently and are applied at officer discretion.
