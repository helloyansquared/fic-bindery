#!/usr/bin/env python3
"""Build the public site from src/.
Usage: python3 build.py https://fictoepub.pages.dev/   (site root, trailing slash)
Writes public/<page>, public/robots.txt, public/sitemap.xml and public/llms.txt.
public/ is what the host serves (Cloudflare Pages: build command empty, output directory `public`).

Structured data (JSON-LD) is generated here from each page's visible text, so the FAQ
markup always matches what readers see. Edit LAST_UPDATED when content changes."""
import sys, re, json, html, pathlib

LAST_UPDATED = "2026-11-25"
SITE = sys.argv[1].rstrip('/') + '/'
ROOT = pathlib.Path(__file__).parent
REPO = "https://github.com/helloyansquared/fic-bindery"
SAME_AS = [REPO, "https://www.tumblr.com/yesyanyan", "https://x.com/yesyanyan"]

# (source file, public path, page kind)
PAGES = [
    ("src/index.html", "", "app"),
    ("src/ao3-to-kindle/index.html", "ao3-to-kindle/", "guide"),
]

FONTS = [("Fraunces", "fraunces-latin-600-normal", 600), ("Fraunces", "fraunces-latin-700-normal", 700),
         ("Instrument Sans", "instrument-sans-latin-400-normal", 400), ("Instrument Sans", "instrument-sans-latin-500-normal", 500),
         ("Instrument Sans", "instrument-sans-latin-600-normal", 600)]

def text(fragment):
    t = re.sub(r'<[^>]+>', '', fragment)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()

def faq_items(s):
    out = []
    for q, a in re.findall(r'<details[^>]*>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>', s, re.S):
        out.append({"@type": "Question", "name": text(q), "acceptedAnswer": {"@type": "Answer", "text": text(a)}})
    return out

def meta(s, name):
    m = re.search(r'<meta name="%s" content="([^"]*)"' % name, s)
    return html.unescape(m.group(1)) if m else ""

def jsonld(s, url, kind):
    title = text(re.search(r'<title>(.*?)</title>', s, re.S).group(1))
    desc = meta(s, "description")
    org = {"@type": "Organization", "@id": SITE + "#org", "name": "FicToEpub", "url": SITE,
           "logo": SITE + "favicon.svg", "sameAs": SAME_AS}
    website = {"@type": "WebSite", "@id": SITE + "#website", "name": "FicToEpub", "url": SITE,
               "publisher": {"@id": SITE + "#org"}, "inLanguage": "en"}
    graph = [org, website]
    if kind == "app":
        graph.append({"@type": "WebApplication", "@id": url + "#app", "name": "FicToEpub – AO3 HTML to EPUB Converter",
                      "url": url, "description": desc, "applicationCategory": "UtilitiesApplication",
                      "operatingSystem": "Any (web browser)",
                      "browserRequirements": "Requires JavaScript. Works in current Chrome, Safari, Firefox and Edge, on desktop and mobile.",
                      "isAccessibleForFree": True, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
                      "featureList": ["Converts AO3 HTML downloads to EPUB 3 with an EPUB 2 NCX table of contents",
                                      "Runs entirely in the browser; files are never uploaded",
                                      "Reads AO3 chapter titles, tags, summary, notes and end notes",
                                      "Generates a cover from the title and author",
                                      "Merges several works or a series into one EPUB"],
                      "dateModified": LAST_UPDATED, "publisher": {"@id": SITE + "#org"}, "isPartOf": {"@id": SITE + "#website"}})
    else:
        h1 = text(re.search(r'<h1>(.*?)</h1>', s, re.S).group(1))
        graph.append({"@type": "Article", "@id": url + "#article", "headline": h1, "description": desc, "url": url,
                      "dateModified": LAST_UPDATED, "datePublished": LAST_UPDATED, "inLanguage": "en",
                      "author": {"@id": SITE + "#org"}, "publisher": {"@id": SITE + "#org"},
                      "isPartOf": {"@id": SITE + "#website"}, "image": SITE + "og.png"})
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "AO3 HTML to EPUB converter", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]})
    faqs = faq_items(s)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": faqs})
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return '<script type="application/ld+json">\n' + data.replace('<', '\\u003c') + '\n</script>'

def build_page(src, path, kind):
    s = (ROOT / src).read_text()
    url = SITE + path
    # self-hosted fonts instead of Google Fonts (no third-party requests)
    s = re.sub(r'<link rel="preconnect"[^\n]*\n<link href="https://fonts.googleapis.com[^\n]*\n',
               '<link rel="preload" href="/fonts/fraunces-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n', s)
    faces = ''.join(f'@font-face{{font-family:"{fam}";src:url(/fonts/{f}.woff2) format("woff2");font-weight:{w};font-display:swap}}\n'
                    for fam, f, w in FONTS)
    s = s.replace('<style>\n', '<style>\n' + faces, 1)
    head = (f'<link rel="canonical" href="{url}">\n<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            f'<meta property="og:url" content="{url}">\n<meta property="og:image" content="{SITE}og.png">\n'
            '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
            '<meta property="og:site_name" content="FicToEpub">\n<meta name="twitter:card" content="summary_large_image">')
    assert '<!--SEO-HEAD-->' in s and '<!--JSONLD-->' in s, src
    s = s.replace('<!--SEO-HEAD-->', head).replace('<!--JSONLD-->', jsonld(s, url, kind))
    out = ROOT / 'public' / path / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s)
    return url

urls = [build_page(*p) for p in PAGES]

(ROOT / 'public/robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
(ROOT / 'public/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{u}</loc><lastmod>{LAST_UPDATED}</lastmod></url>\n' for u in urls) + '</urlset>\n')
(ROOT / 'public/llms.txt').write_text(f"""# FicToEpub

> Free in-browser converter that turns AO3 (Archive of Our Own) HTML downloads into EPUB files. No upload, no account, no ads.

- URL: {SITE}
- Input: .html files downloaded with AO3's own Entire Work → Download → HTML button (any saved HTML page also works)
- Output: EPUB 3 with an EPUB 2 (NCX) table of contents, one chapter per AO3 chapter, a work info page (tags, summary, notes) and a generated cover
- Can merge several works or a whole series into one EPUB
- Files are processed locally in the browser; nothing is sent to a server
- Does not scrape or download anything from AO3
- Works on phones, tablets and computers; no install
- Kindle: send the EPUB with Amazon's Send to Kindle (web up to 200 MB, email up to 50 MB)
- Context: since AO3's return from an outage on 15 November 2026, readers report AO3 downloads are HTML-only (as of {LAST_UPDATED})
- Source code: {REPO}
- Not affiliated with AO3 or the Organization for Transformative Works

## Pages

- [AO3 HTML to EPUB converter]({SITE}): the tool, how-to, comparison with Calibre and online converters, FAQ
- [How to send AO3 fics to Kindle]({SITE}ao3-to-kindle/): Send to Kindle by web, app and email, size limits, troubleshooting

## Also by the same maker

- [FicWrapped](https://ficwrapped.yansquared.com/): AO3 Wrapped, your year in fic from your own AO3 History
- [BotToBook](https://bottobook.yansquared.com/): Character.AI data export to PDF and EPUB books
""")
print('built for', SITE, '->', ', '.join(urls))
