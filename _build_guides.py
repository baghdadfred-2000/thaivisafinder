#!/usr/bin/env python3
# Generates 18 Thailand visa guide HTML pages from the uploaded .docx files,
# wrapped in the standard ThaiVisaFinder site chrome (topbar nav + fgrid footer +
# Adsterra banner above footer), with a rich guide-style body in the site palette.
import glob, os, re, html

SRC_DIR = "/sessions/trusting-pensive-gauss/mnt/uploads"
OUT_DIR = "/sessions/trusting-pensive-gauss/mnt/thaivisafinder"

from docx import Document

# ---- SEO slugs keyed by source-file number ----
SLUGS = {
 "01":"thailand-visa-exemption",
 "02":"thailand-tourist-visa-tr",
 "03":"destination-thailand-visa-dtv",
 "04":"non-o-retirement-visa",
 "05":"non-oa-long-stay-retirement-visa",
 "06":"non-o-x-retirement-visa",
 "07":"ltr-wealthy-pensioner-visa",
 "08":"ltr-work-from-thailand-visa",
 "09":"ltr-wealthy-global-citizen-visa",
 "10":"ltr-highly-skilled-professional-visa",
 "11":"thailand-privilege-elite-visa",
 "12":"marriage-non-o-visa",
 "13":"family-dependent-non-o-visa",
 "14":"non-b-work-permit-visa",
 "15":"education-ed-visa",
 "16":"smart-visa",
 "17":"medical-non-o-visa",
 "18":"volunteer-non-o-visa",
}
# Short eyebrow label per number
EYEBROWS = {
 "01":"Short-stay entry","02":"Short-stay visa","03":"Remote work & soft power",
 "04":"Retirement route","05":"Retirement route","06":"Retirement route",
 "07":"Long-Term Resident","08":"Long-Term Resident","09":"Long-Term Resident",
 "10":"Long-Term Resident","11":"Premium membership","12":"Family route",
 "13":"Family route","14":"Local work route","15":"Study route",
 "16":"Skilled & startup route","17":"Special-purpose route","18":"Special-purpose route",
}

def esc(s): return html.escape(s, quote=True)

def runs_to_html(p):
    """Convert a paragraph's runs to HTML preserving bold/italic; escape text."""
    out=[]
    for r in p.runs:
        t=r.text
        if not t: continue
        t=esc(t)
        if r.bold: t="<strong>%s</strong>"%t
        if r.italic: t="<em>%s</em>"%t
        out.append(t)
    s="".join(out)
    if not s.strip():
        s=esc(p.text)
    return s

def slugify_anchor(t):
    a=re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
    return a[:60]

def clean_title(t):
    return re.sub(r'^\s*\d+\.\s*','',t).strip()

def first_sentences(text, limit=158):
    text=re.sub(r'\s+',' ',text).strip()
    if len(text)<=limit: return text
    cut=text[:limit]
    # trim to last sentence end or word boundary
    m=list(re.finditer(r'[.!?]\s',cut))
    if m and m[-1].end()>60:
        return cut[:m[-1].end()].strip()
    return cut.rsplit(' ',1)[0].strip()+'…'

def parse_doc(path):
    d=Document(path)
    paras=[p for p in d.paragraphs]
    title=None; updated=None
    sections=[]  # {title, id, blocks}
    cur=None
    pending_list=None
    intro_text=""

    def flush_list():
        nonlocal pending_list
        if pending_list is not None and cur is not None:
            cur["blocks"].append(("ul",pending_list))
        pending_list=None

    for p in paras:
        t=p.text.strip()
        style=p.style.name if p.style else "None"
        if not t:
            continue
        if style=="Heading 1" and title is None:
            title=clean_title(t); continue
        if title is not None and updated is None and style not in ("Heading 1","Heading 2","Heading 3","List Paragraph"):
            # first normal paragraph after title = "Updated ..." line
            if re.match(r'(?i)updated', t):
                updated=t; continue
        if style=="Heading 2":
            flush_list()
            cur={"title":t,"id":slugify_anchor(t),"blocks":[]}
            sections.append(cur); continue
        if style=="Heading 3":
            flush_list()
            if cur is not None: cur["blocks"].append(("h3",runs_to_html(p),t))
            continue
        if style=="List Paragraph":
            if pending_list is None: pending_list=[]
            pending_list.append(runs_to_html(p)); continue
        # normal paragraph
        flush_list()
        if cur is not None:
            cur["blocks"].append(("p",runs_to_html(p)))
            if cur["title"].lower().startswith("introduction") and not intro_text:
                intro_text=p.text.strip()
    flush_list()
    if updated is None: updated="Updated July 2026"
    return title, updated, sections, intro_text

# ---------- rendering helpers ----------
CHECK_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
X_SVG='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>'

def render_generic(blocks):
    out=[]
    for b in blocks:
        if b[0]=="p": out.append("      <p>%s</p>"%b[1])
        elif b[0]=="h3": out.append("      <h3>%s</h3>"%b[1])
        elif b[0]=="ul":
            lis="".join("<li>%s</li>"%i for i in b[1])
            out.append("      <ul>%s</ul>"%lis)
    return "\n".join(out)

def render_proscons(blocks):
    """blocks contain h3 Pros + ul, h3 Cons + ul (and maybe intro p)."""
    pros=[]; cons=[]; lead=[]; mode=None
    for b in blocks:
        if b[0]=="h3":
            low=b[2].lower()
            mode="pros" if "pro" in low else ("cons" if "con" in low else None)
        elif b[0]=="ul":
            if mode=="pros": pros=b[1]
            elif mode=="cons": cons=b[1]
        elif b[0]=="p":
            lead.append("      <p>%s</p>"%b[1])
    if not pros and not cons:
        return render_generic(blocks)
    prosli="".join("<li>%s<span>%s</span></li>"%(CHECK_SVG,i) for i in pros)
    consli="".join("<li>%s<span>%s</span></li>"%(X_SVG,i) for i in cons)
    html_out="\n".join(lead)+"\n" if lead else ""
    html_out+='''      <div class="proscons">
        <div class="pc pc-pros"><h3>Pros</h3><ul>%s</ul></div>
        <div class="pc pc-cons"><h3>Cons</h3><ul>%s</ul></div>
      </div>'''%(prosli,consli)
    return html_out

def render_checklist(blocks):
    out=[]
    for b in blocks:
        if b[0]=="p": out.append("      <p>%s</p>"%b[1])
        elif b[0]=="ul":
            lis="".join('<li>%s<span>%s</span></li>'%(CHECK_SVG,i) for i in b[1])
            out.append('      <ul class="checklist">%s</ul>'%lis)
        elif b[0]=="h3": out.append("      <h3>%s</h3>"%b[1])
    return "\n".join(out)

def render_section(sec, idx):
    title=sec["title"]; low=title.lower()
    if "pros and cons" in low:
        body=render_proscons(sec["blocks"])
    elif "requirements checklist" in low or (low.startswith("requirements") and "checklist" in low):
        body=render_checklist(sec["blocks"])
    else:
        body=render_generic(sec["blocks"])
    wide = "detailed requirements" in low or "pros and cons" in low
    wrapcls="wrap"
    eyebrow=esc(title)
    return '''<section class="block" id="{id}">
  <div class="{wrap}">
    <div class="eyebrow-mark"><span>{eyebrow}</span></div>
    <h2>{title}</h2>
{body}
  </div>
</section>'''.format(id=sec["id"],wrap=wrapcls,eyebrow=eyebrow,title=esc(title),body=body)

# ---------- page template ----------
HEAD = r'''<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<style class="xad-off">.xadr,.ad-rail,.side-rail,.rail-ad,.wz-rail{{display:none!important}}</style>
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/favicon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>(function(){{try{{var t=localStorage.getItem("tvf-theme");if(t==="light"||t==="dark"){{document.documentElement.setAttribute("data-theme",t);}}}}catch(e){{}}}})();function toggleTheme(){{var h=document.documentElement,n=h.getAttribute("data-theme")==="dark"?"light":"dark";h.setAttribute("data-theme",n);try{{localStorage.setItem("tvf-theme",n);}}catch(e){{}}}}</script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#181845">
<title>{seo_title}</title>
<meta name="description" content="{meta_desc}">
<meta name="author" content="Uncle Pong's Thailand (Genext Information Systems)">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="https://thaivisafinder.com/{slug}.html">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Uncle Pong's Thailand Visa Finder">
<meta property="og:title" content="{seo_title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="https://thaivisafinder.com/{slug}.html">
<meta property="og:image" content="https://thaivisafinder.com/og-image.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{seo_title}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://thaivisafinder.com/og-image.jpg">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":{jl_head},"description":{jl_desc},"author":{{"@type":"Organization","name":"Genext Information Systems"}},"publisher":{{"@type":"Organization","name":"Uncle Pong's Thailand Visa Finder"}},"datePublished":"2026-07-16","dateModified":"2026-07-16","mainEntityOfPage":"https://thaivisafinder.com/{slug}.html"}}
</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,700;12..96,800&family=Hanken+Grotesk:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Spline+Sans+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{{
  --ink:#1B1A38; --ink-soft:#4D4B6B; --paper:#FBF9F3; --paper-2:#EFEDE4;
  --surface:#FFFFFF; --jade:#26276B; --jade-deep:#181845; --jade-soft:#E6E6F3;
  --mango:#C8102E; --line:#E6E3D7; --radius:18px; --maxw:820px;
}}
*{{box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{margin:0;background:var(--paper);color:var(--ink);
  font-family:'Hanken Grotesk',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
  font-size:17px;line-height:1.65;}}
a{{color:var(--jade);}}
img,svg{{max-width:100%;}}
.wrap{{width:100%;max-width:var(--maxw);margin:0 auto;padding:0 22px;}}
.wrap-wide{{width:100%;max-width:940px;margin:0 auto;padding:0 22px;}}
.skip{{position:absolute;left:-9999px;top:0;background:var(--jade);color:#fff;padding:10px 16px;border-radius:8px;}}
.skip:focus{{left:12px;top:12px;z-index:50;}}

header.topbar{{background:rgba(255,246,233,.9);backdrop-filter:blur(10px);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20;}}
.topbar .inner{{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 0;}}
.brand{{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--ink);}}
.brand .logo{{width:40px;height:40px;border-radius:50%;flex:0 0 auto;overflow:hidden;background:url('logo.png') center/cover no-repeat;box-shadow:0 1px 3px rgba(0,0,0,.18);}}
.brand .bt{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:.78rem;letter-spacing:.08em;color:var(--mango);text-transform:uppercase;display:block;line-height:1;margin-bottom:2px;}}
.brand .bs{{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:1.02rem;color:var(--ink);display:block;line-height:1.15;}}
.topnav{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;}}
.topnav a{{text-decoration:none;color:var(--ink-soft);font-weight:600;font-size:.95rem;padding:8px 10px;border-radius:9px;}}
.topnav a:hover{{background:var(--jade-soft);color:var(--jade);}}
.topnav a.cta{{background:var(--mango);color:#fff;}}
.topnav a.cta:hover{{background:#9C0B22;color:#fff;}}

/* ---------- HERO ---------- */
.ghero{{background:linear-gradient(160deg,var(--jade-deep) 0%,var(--jade) 100%);color:#fff;padding:56px 0 44px;position:relative;overflow:hidden;}}
.ghero .eyebrow{{display:inline-block;font-family:'Bricolage Grotesque',sans-serif;text-transform:uppercase;letter-spacing:.14em;font-size:.72rem;font-weight:700;color:#F4B8C1;margin-bottom:12px;}}
.ghero h1{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(1.9rem,4.2vw,2.9rem);line-height:1.1;margin:0 0 .5em;max-width:20ch;color:#fff;}}
.ghero p.sub{{font-size:1.12rem;color:#D9D9EC;max-width:60ch;margin:0 0 20px;}}
.ghero .byline{{font-size:.9rem;color:#B9B9D6;display:flex;gap:.6rem;flex-wrap:wrap;align-items:center;margin-top:14px;}}
.ghero .byline .dot{{opacity:.5;}}
.gbtn{{display:inline-flex;align-items:center;gap:.5rem;background:var(--mango);color:#fff;font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:1rem;padding:12px 22px;border-radius:999px;text-decoration:none;transition:background .15s,transform .15s;}}
.gbtn:hover{{background:#9C0B22;color:#fff;transform:translateY(-1px);}}

/* ---------- TOC ---------- */
.toc{{background:var(--surface);border:1px solid var(--line);border-left:4px solid var(--mango);border-radius:12px;padding:20px 24px;margin:-26px auto 30px;position:relative;z-index:5;box-shadow:0 18px 40px -26px rgba(70,45,10,.30);}}
.toc p.label{{font-family:'Bricolage Grotesque',sans-serif;text-transform:uppercase;letter-spacing:.12em;font-size:.7rem;font-weight:700;color:var(--mango);margin:0 0 10px;}}
.toc ol{{columns:2;column-gap:2rem;margin:0;padding-left:1.1rem;font-size:.95rem;}}
.toc li{{margin-bottom:.5rem;break-inside:avoid;}}
.toc a{{text-decoration:none;color:var(--ink);}}
.toc a:hover{{color:var(--mango);}}

/* ---------- SECTIONS ---------- */
main{{padding:6px 0 10px;}}
section.block{{padding:26px 0;}}
section.block + section.block{{margin-top:2px;}}
.eyebrow-mark{{display:flex;align-items:center;gap:.7rem;margin-bottom:.7rem;}}
.eyebrow-mark span{{font-family:'Bricolage Grotesque',sans-serif;text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:700;color:var(--mango);white-space:nowrap;}}
.eyebrow-mark::after{{content:"";flex:1;height:1px;background:var(--line);}}
h1{{font-family:'Bricolage Grotesque',sans-serif;}}
h2{{font-family:'Bricolage Grotesque',sans-serif;font-weight:800;font-size:clamp(1.4rem,3vw,1.9rem);line-height:1.15;margin:.1em 0 .5em;color:var(--ink);}}
h3{{font-family:'Bricolage Grotesque',sans-serif;font-weight:700;font-size:1.18rem;margin:1.5em 0 .35em;color:var(--jade);}}
p{{margin:.7em 0;}}
ul{{margin:.6em 0;padding-left:1.25em;}}
li{{margin:.4em 0;}}
strong{{color:var(--ink);}}
.lede{{font-size:1.16rem;}}
.lede::first-letter{{font-family:'Bricolage Grotesque',sans-serif;font-size:3.3rem;float:left;line-height:.8;padding:.06em .12em 0 0;color:var(--mango);font-weight:800;}}

/* ---------- PROS / CONS ---------- */
.proscons{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:1.1em 0;}}
.pc{{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;}}
.pc h3{{margin:.1em 0 .5em;font-size:1.05rem;}}
.pc-pros{{border-top:3px solid #1F7A4D;}}
.pc-cons{{border-top:3px solid var(--mango);}}
.pc ul{{list-style:none;margin:0;padding:0;}}
.pc li{{display:flex;gap:.6rem;align-items:flex-start;margin:.5rem 0;font-size:.98rem;}}
.pc li svg{{width:20px;height:20px;flex:0 0 auto;margin-top:.15rem;}}
.pc-pros li svg{{color:#1F7A4D;}}
.pc-cons li svg{{color:var(--mango);}}

/* ---------- CHECKLIST ---------- */
ul.checklist{{list-style:none;margin:1.1em 0;padding:0;}}
ul.checklist li{{display:flex;gap:.7rem;align-items:flex-start;margin:.6rem 0;font-size:1rem;}}
ul.checklist li svg{{width:20px;height:20px;flex:0 0 auto;margin-top:.15rem;color:var(--jade);}}

/* ---------- CTA BAND ---------- */
.cta-band{{background:var(--jade-deep);color:#fff;border-radius:16px;padding:30px 26px;text-align:center;margin:34px 0 6px;}}
.cta-band h3{{color:#fff;margin:0 0 .4em;font-size:1.35rem;}}
.cta-band p{{color:#D3D3E6;max-width:46ch;margin:0 auto 1.1rem;}}

/* ---------- FOOTER ---------- */
footer{{background:var(--jade-deep);color:#cfcfe6;margin-top:14px;padding:34px 0 26px;}}
footer .fgrid{{display:flex;flex-wrap:wrap;gap:28px;justify-content:space-between;}}
footer h4{{font-family:'Bricolage Grotesque',sans-serif;color:#fff;font-size:.95rem;margin:0 0 10px;}}
footer a{{color:#cfcfe6;text-decoration:none;display:block;padding:3px 0;font-size:.95rem;}}
footer a:hover{{color:#fff;text-decoration:underline;}}
.brand-f{{display:flex;align-items:center;gap:10px;color:#fff;font-family:'Bricolage Grotesque',sans-serif;font-weight:800;margin-bottom:8px;}}
.brand-f .logo{{width:30px;height:30px;border-radius:50%;background:#fff center/cover no-repeat;background-image:url('logo.png');}}
.legal{{border-top:1px solid rgba(255,255,255,.12);margin-top:24px;padding-top:16px;font-size:.82rem;color:#9c9cc0;line-height:1.6;}}

.theme-toggle{{display:inline-flex;align-items:center;justify-content:center;width:38px;height:38px;padding:0;margin-left:4px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:10px;cursor:pointer;transition:background .15s,color .15s;flex:0 0 auto;}}
.theme-toggle:hover{{background:var(--paper-2);}}
.theme-toggle svg{{width:18px;height:18px;}}
.theme-toggle .i-sun{{display:none;}}
.theme-toggle .i-moon{{display:block;}}

@media(max-width:640px){{ .toc ol{{columns:1;}} .proscons{{grid-template-columns:1fr;}} .topnav a.hide-sm{{display:none;}} }}
@media(prefers-reduced-motion:reduce){{ html{{scroll-behavior:auto;}} }}
</style>
<style id="tvf-theme">
:root[data-theme="dark"]{{
  --ink:#E9EBEF; --ink-soft:#9AA2AF;
  --paper:#0B0E13; --paper-2:#141922; --surface:#20262F;
  --jade:#6C93F2; --jade-deep:#080A0E; --jade-soft:#262D3A;
  --mango:#E3AE4E; --line:#333C4A;
  background:#0B0E13; color-scheme:dark;
}}
:root[data-theme="dark"] .topbar{{background:rgba(11,14,19,.88);}}
:root[data-theme="dark"] .ghero{{background:linear-gradient(160deg,#05070A 0%,#161C27 100%);}}
:root[data-theme="dark"] .ghero .eyebrow{{color:#F1C56B;}}
:root[data-theme="dark"] .eyebrow-mark span{{color:#F1C56B;}}
:root[data-theme="dark"] .gbtn,:root[data-theme="dark"] .topnav a.cta{{color:#17110A;}}
:root[data-theme="dark"] .gbtn:hover{{background:#F1C56B;color:#17110A;}}
:root[data-theme="dark"] strong{{color:var(--ink);}}
:root[data-theme="dark"] .theme-toggle .i-sun{{display:block;}}
:root[data-theme="dark"] .theme-toggle .i-moon{{display:none;}}
:root[data-theme="dark"] .cta-band p{{color:#C7CBD6;}}
</style>
</head>
<body>
<a href="#main" class="skip">Skip to content</a>
<header class="topbar">
  <div class="wrap inner">
    <a class="brand" href="index.html" aria-label="Uncle Pong's Thailand Visa Finder home">
      <span class="logo" role="img" aria-label="Uncle Pong logo"></span>
      <span><span class="bt">Uncle Pong's</span><span class="bs">Thailand Visa Finder</span></span>
    </a>
    <nav class="topnav" aria-label="Primary">
      <a href="index.html">Home</a>
      <a href="city-guide.html" class="hide-sm">City Guide</a>
      <a href="about.html" class="hide-sm">About</a>
      <a href="contact.html" class="hide-sm">Contact</a>
      <button class="theme-toggle" type="button" onclick="toggleTheme()" aria-label="Toggle light or dark theme" title="Toggle light/dark theme"><svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg><svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v1.5M12 20.5V22M4.2 4.2l1.1 1.1M18.7 18.7l1.1 1.1M2 12h1.5M20.5 12H22M4.2 19.8l1.1-1.1M18.7 5.3l1.1-1.1"/></svg></button>
      <a href="index.html" class="cta">Find My Visa</a>
    </nav>
  </div>
</header>

<header class="ghero">
  <div class="wrap">
    <span class="eyebrow">{eyebrow}</span>
    <h1>{h1}</h1>
    <p class="sub">{hero_sub}</p>
    <a class="gbtn" href="index.html">Find my visa &rarr;</a>
    <div class="byline"><span>Uncle Pong's Thailand Visa Finder</span><span class="dot">&middot;</span><span>{updated}</span><span class="dot">&middot;</span><span>Independent &amp; commission-free</span></div>
  </div>
</header>

<main id="main">
  <div class="wrap">
    <nav class="toc" aria-label="On this page">
      <p class="label">On this page</p>
      <ol>
{toc}
      </ol>
    </nav>
    <p class="lede">{lede}</p>
  </div>
{sections}
'''

FOOTER = r'''
<!-- ===== AD BANNER (above footer) ===== -->
<style>
  .ad-banner-zone{width:100%;margin:44px auto 0;padding:0 22px;box-sizing:border-box;display:flex;justify-content:center;}
  .ad-banner-zone iframe{border:0;display:block;overflow:hidden;max-width:100%;}
  @media(max-width:768px){.ad-banner-zone{padding:0 10px;}.ad-banner-zone iframe{overflow-x:auto;}}
</style>
<div class="ad-banner-zone" aria-label="Advertisement">
  <iframe title="Advertisement" width="728" height="90" scrolling="no" frameborder="0" srcdoc='<body style="margin:0"><script type="text/javascript">atOptions={"key":"167029ed1bd365dff490be4d9d295756","format":"iframe","height":90,"width":728,"params":{}};</script><script type="text/javascript" src="https://www.highperformanceformat.com/167029ed1bd365dff490be4d9d295756/invoke.js"></script><style class="xadr-fix">.xadr{position:absolute!important;top:auto!important;bottom:calc(100% + 100px)!important;width:160px!important;z-index:40;line-height:0}.xadr iframe{border:0;display:block;overflow:hidden}.xadr-l{left:calc(50% - 616px)!important;right:auto!important}.xadr-r{right:calc(50% - 616px)!important;left:auto!important}@media(max-width:1240px){.xadr{display:none!important}}[data-xadr-footer]{position:relative}</style>
</body>'></iframe>
</div>

<footer data-xadr-footer><div class="xadr xadr-l" aria-label="Advertisement"><iframe title="Advertisement" width="160" height="300" scrolling="no" frameborder="0" marginwidth="0" marginheight="0" style="border:0;display:block;overflow:hidden" srcdoc='<body style="margin:0;overflow:hidden"><script type="text/javascript">atOptions = {"key":"9fb5ed3f58327b9ed9e9acd4af62f648","format":"iframe","height":300,"width":160,"params":{}};</script><script type="text/javascript" src="https://www.highperformanceformat.com/9fb5ed3f58327b9ed9e9acd4af62f648/invoke.js"></script></body>'></iframe></div><div class="xadr xadr-r" aria-label="Advertisement"><iframe title="Advertisement" width="160" height="300" scrolling="no" frameborder="0" marginwidth="0" marginheight="0" style="border:0;display:block;overflow:hidden" srcdoc='<body style="margin:0;overflow:hidden"><script type="text/javascript">atOptions = {"key":"9fb5ed3f58327b9ed9e9acd4af62f648","format":"iframe","height":300,"width":160,"params":{}};</script><script type="text/javascript" src="https://www.highperformanceformat.com/9fb5ed3f58327b9ed9e9acd4af62f648/invoke.js"></script></body>'></iframe></div>
  <div class="wrap">
    <div class="fgrid">
      <div style="max-width:300px;">
        <div class="brand-f"><span class="logo" role="img" aria-label="Uncle Pong logo"></span> Uncle Pong's</div>
        <p style="margin:0;color:#b6b6d4;">Straight talk on staying in Thailand legally and happily &mdash; built to inform, never to sell you a visa package. &#128591;</p>
      </div>
      <div>
        <h4>The tools</h4>
        <a href="index.html">Visa Finder</a>
        <a href="index.html#faq">Visa FAQ</a>
        <a href="city-guide.html">City Guide</a>
        <a href="https://thaiholidaybudget.com/" target="_blank" rel="noopener">Budget Estimator &#8599;</a>
      </div>
      <div>
        <h4>Site &amp; legal</h4>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="terms.html">Terms &amp; Disclaimer</a>
      </div>
    </div>
    <div class="legal">
      <b>For information &amp; planning only.</b> Not legal advice and not affiliated with the Thai government, any embassy, or any visa agency. Immigration rules, costs and eligibility change without notice and are subject to official discretion &mdash; please do your own research and verify with official sources or a qualified professional. Visa data reviewed July 2026. &nbsp;|&nbsp; &copy; 2026 Genext Information Systems. All rights reserved.
    </div>
  </div>
</footer>
</body>
</html>'''

import json
def build():
    files=sorted(glob.glob(os.path.join(SRC_DIR,"*.docx")))
    written=[]
    for f in files:
        base=os.path.basename(f)
        num=base[:2]
        slug=SLUGS[num]
        title,updated,sections,intro=parse_doc(f)
        # meta description from intro
        desc=first_sentences(intro or title, 158)
        seo_title="%s (2026 Guide) | ThaiVisaFinder" % title
        # hero sub: a slightly longer intro snippet
        hero_sub=esc(first_sentences(intro or title, 230))
        # lede = full first intro paragraph; remove it from Introduction section to avoid duplication
        lede_html=""
        for sec in sections:
            if sec["title"].lower().startswith("introduction"):
                # pull first p as lede, keep the rest
                newblocks=[]; used=False
                for b in sec["blocks"]:
                    if not used and b[0]=="p":
                        lede_html=b[1]; used=True; continue
                    newblocks.append(b)
                sec["blocks"]=newblocks
                break
        if not lede_html:
            lede_html=esc(intro or title)
        # TOC (skip empty Introduction if it now has no blocks -> still list it)
        toc_items=[]
        rendered_sections=[]
        for i,sec in enumerate(sections):
            # drop a now-empty introduction section header (its lede shown above)
            if sec["title"].lower().startswith("introduction") and not sec["blocks"]:
                continue
            toc_items.append('        <li><a href="#%s">%s</a></li>'%(sec["id"],esc(sec["title"])))
            rendered_sections.append(render_section(sec,i))
        # add CTA band before footer inside last section area
        cta='''  <div class="wrap">
    <div class="cta-band">
      <h3>Not sure this is your best route?</h3>
      <p>Answer a few honest questions and Uncle Pong will weigh all 18 legal Thailand visas against your situation &mdash; free, no account, no commission.</p>
      <a class="gbtn" href="index.html">Take the free Visa Finder &rarr;</a>
    </div>
  </div>
</main>'''
        head=HEAD.format(
            seo_title=esc(seo_title), meta_desc=esc(desc), slug=slug,
            jl_head=json.dumps(title), jl_desc=json.dumps(desc),
            eyebrow=esc(EYEBROWS[num]), h1=esc(title), hero_sub=hero_sub,
            updated=esc(updated), toc="\n".join(toc_items),
            lede=lede_html, sections="\n".join(rendered_sections))
        page=head+"\n"+cta+FOOTER
        out=os.path.join(OUT_DIR,slug+".html")
        with open(out,"w",encoding="utf-8") as fh:
            fh.write(page)
        written.append((slug+".html",title,len(sections)))
    return written

if __name__=="__main__":
    w=build()
    for fn,t,n in w:
        print(f"{fn:42s} <- {t[:48]}")
    print("TOTAL:",len(w))
