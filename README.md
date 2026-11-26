# FicToEpub — AO3 HTML to EPUB converter

**Use it here: https://fictoepub.yansquared.com/**

To convert an AO3 HTML download to EPUB, open the work on AO3, click **Entire Work**, then **Download → HTML**. Drop that file into [FicToEpub](https://fictoepub.yansquared.com/) and press **Make EPUB**. The EPUB is built in your browser with chapters, a table of contents and a cover. Nothing is uploaded, and you don't need an account or any software.

Since AO3 came back from its outage on 15 November 2026, readers report that AO3 downloads are HTML-only (as of 25 November 2026). FicToEpub turns that HTML into the EPUB you'd normally get.

## What it does

- **0 files uploaded:** conversion runs entirely in the browser (plain JavaScript, no server).
- **EPUB 3** with an EPUB 2 (NCX) table of contents, so older e-readers work too. Test output passes [EPUBCheck](https://github.com/w3c/epubcheck).
- **Reads AO3's structure:** one chapter per AO3 chapter, plus a work info page (tags, summary, notes) and end notes.
- **Generated cover** from the title and author.
- **Merge** several works or a whole series into one EPUB, with a nested table of contents.
- Works on phones, tablets and computers. Any other saved HTML page works too (chapters are split on headings).
- Does **not** scrape or download anything from AO3. You download the work yourself with AO3's own button.

## Reading on a Kindle

Convert to EPUB first, then send it with Amazon's Send to Kindle (web upload up to 200 MB, or email up to 50 MB). Step-by-step: [How to send AO3 fics to Kindle](https://fictoepub.yansquared.com/ao3-to-kindle/).

## FicToEpub vs Calibre

Calibre works well on a computer: add the .html file, click **Convert books**, choose EPUB. FicToEpub needs no install, works on phones, and keeps AO3's tags, summary and notes on a separate work info page.

## Develop

The site is plain static files in `public/`. Edit the pages in `src/`, then run:

```
python3 build.py https://fictoepub.yansquared.com/
```

`build.py` writes `public/` pages, `robots.txt`, `sitemap.xml` and `llms.txt`, and generates the JSON-LD (FAQ markup comes from the visible FAQ text). Cloudflare Pages serves `public/` with no build step.

---

Not affiliated with Archive of Our Own or the Organization for Transformative Works. Fanworks belong to their creators: convert for personal reading only, and leave kudos and comments on AO3.
