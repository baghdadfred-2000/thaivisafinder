# Google SEO Report & Action Plan — thaivisafinder.com
*Prepared June 2026. Applies to the single-page tool in `index.html`.*

---

## 1. Page analysis & target keyword

| | |
|---|---|
| **Page type** | Homepage + interactive tool (`WebApplication`) |
| **Primary keyword** | **Thailand visa finder** / "which Thailand visa is right for me" |
| **Search intent** | Commercial-investigation + informational — people researching which long-stay Thai visa fits them |
| **Secondary keywords** | best Thailand visa 2026, Thailand retirement visa, DTV visa, LTR visa Thailand, Thailand digital nomad visa, Thailand marriage visa, Thailand Privilege, Thailand long-stay visa cost |
| **Entities** | Thailand, DTV, LTR, Non-O, Thailand Privilege, BOI, Royal Thai immigration, Pattaya/Chiang Mai/Phuket/Krabi/Bangkok |

The domain (`thaivisafinder.com`) is an exact match for the head keyword, which is an asset — the title, H1, and first paragraph all reinforce "Thailand visa finder" naturally without stuffing.

---

## 2. Key Google SEO changes made (and why)

**`<head>` / meta**
- **Title** → `Thailand Visa Finder: Which Visa Is Right for You? 2026` (55 chars). Keyword first, year for freshness, click-worthy question. *Helps relevance + CTR.*
- **Meta description** (~145 chars) naming the concrete routes (retirement, DTV, LTR, marriage, Privilege). *Wins clicks and matches long-tail queries.*
- **Canonical** → `https://thaivisafinder.com/`. *Prevents duplicate-URL dilution (trailing slash, query params, www vs non-www).*
- **Robots** → `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`. *Allows large image thumbnails and full snippets in regular results and AI Overviews.*
- **Open Graph + Twitter** cards with a real **1200×630 `og-image.jpg`**. *Controls how the link looks when shared; better social CTR.*

**Structured data (JSON-LD `@graph`)** — Google's preferred format:
- `Organization` + `WebSite` (publisher/brand identity for the knowledge graph).
- `WebApplication` (free travel tool — accurate page-type signal).
- `FAQPage` with 5 genuine Q&As. *Strong AI-Overview / featured-snippet fuel; high entity density.*

**Content / E-E-A-T / Helpful Content**
- Added a visible **FAQ section** answering the highest-volume questions (best retirement visa, working on DTV, visa-free days in 2026, cheapest visa, cost of living). Question-style H2/H3 with definitive early answers — exactly what AI Overviews extract. The visible text mirrors the FAQ schema (required).
- Reinforced **independence/trust** signals (not affiliated with government or agencies; links to official MFA/BOI/e-Visa sources; "reviewed June 2026"). *E-E-A-T for a YMYL topic (immigration is money/legal-adjacent).*
- One clear **H1** in the hero containing the keyword; logical H2→H3 throughout.

**Technical**
- `lang="en"`, UTF-8, responsive viewport already present (mobile-first ready).
- `color-scheme: light only` + per-section backgrounds (also fixes the dark-mode contrast bug).
- Internal link added to the FAQ from the footer; cross-link to the sister site.

---

## 3. robots.txt

Shipped in the package as `robots.txt` (upload to site root). It allows Google, Googlebot-Image and `Google-Extended` (AI Overviews) full access, allows helpful AI search bots (OAI-SearchBot, PerplexityBot, ClaudeBot) for citation visibility, never blocks CSS/JS/images, blocks only private/parametered paths, and declares the sitemap.

## 4. sitemap.xml

Shipped as `sitemap.xml`. Today it lists only the homepage, because About/Privacy/Terms/FAQ are **client-side views at the same URL** — they are not separately indexable. The commented block shows the entries to enable once you split them into real pages.

---

## 5. The one structural recommendation that matters most

**The site is a JavaScript single-page app.** Google *can* render JS, so the homepage will index fine, but:

- **The About / Privacy / Terms / FAQ "pages" share one URL** (`/`) and only appear after a click, so they can't rank as their own pages and can't be deep-linked. **Recommendation:** give each a real URL (`/about`, `/faq`, `/privacy`, `/terms`, `/accessibility`) — either as separate static HTML files or via server/static-host routing — then add them to the sitemap (template already included). The FAQ especially deserves its own indexable page.
- **Destination photos are CSS background-images**, which Google Images can't index. For image SEO, switch the location cards to `<img src="/images/krabi.jpg" alt="Pi Leh lagoon near Krabi, Thailand" width="900" height="563" loading="lazy">`. The files are already in `/images/`.
- **Consider light pre-rendering** (or a static export) so the hero H1 and FAQ are in the initial HTML, not just after JS runs — marginally safer for crawling and faster First Contentful Paint.

---

## 6. Core Web Vitals notes

- Single self-contained file = no render-blocking third-party JS. Good.
- Fonts load from Google Fonts with `display=swap` (no invisible-text delay). Optionally self-host the two fonts to shave a connection.
- Embedded base64 images inflate the HTML to ~650 KB; moving the four photos to external `/images/` files (and lazy-loading them) reduces initial payload and improves LCP/caching.
- All media sit in fixed-aspect-ratio containers, so CLS should be near zero.

---

## 7. Post-launch Google action plan

1. **Upload** `index.html`, `robots.txt`, `sitemap.xml` and `/images/` to the root of thaivisafinder.com.
2. **Verify the domain** in [Google Search Console](https://search.google.com/search-console) (DNS TXT record is the most robust; pick **non-www** `https://thaivisafinder.com` as primary and 301-redirect www → non-www at your host).
3. **Submit the sitemap** in GSC → Sitemaps → `sitemap.xml`.
4. **URL Inspection → Request indexing** for the homepage.
5. **Test rich results:** run the homepage through the [Rich Results Test](https://search.google.com/test/rich-results) and confirm `WebApplication`, `Organization` and `FAQPage` parse with no errors.
6. **PageSpeed Insights** + **Mobile-Friendly** check; address any LCP/CLS flags (mainly the image-payload note above).
7. **Link GA4 ↔ Search Console** for query/landing-page data.
8. **Monitor** the Coverage/Pages, Core Web Vitals, and Rich Results reports weekly for the first month.
9. **Freshness & E-E-A-T:** keep the "reviewed June 2026" date current as visa rules change (the 60→30-day exemption rollback is the live one to watch), add an author/editorial note, and publish supporting explainer pages ("DTV vs LTR vs Privilege", "cost of retiring in Thailand 2026") that internally link back to the finder.
10. **Redirects:** if you change any URLs later (e.g., splitting out `/faq`), add 301s from old to new.

**Tools:** Google Search Console · PageSpeed Insights · Rich Results Test · Mobile-Friendly Test.

---

## 8. Honest caveats

- I optimized the existing single-page build rather than pasting a 650 KB HTML dump into chat; all changes are live in `index.html`.
- FAQ rich-result *snippets* are now mostly limited by Google to authoritative gov/health sites, so treat the `FAQPage` schema mainly as AI-Overview/understanding fuel rather than a guaranteed SERP feature.
- This is a YMYL (immigration) topic; sustained rankings will depend on demonstrable trust and accuracy over time, not just on-page tags. Keep the data current and the independence visible.
