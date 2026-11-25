# Fic Bindery — AO3 HTML to EPUB converter

Free, private, in-browser converter that turns the HTML file you download from Archive of Our Own (AO3) into a clean EPUB with chapters, a table of contents, a work-info page and a generated cover. Nothing is uploaded: the EPUB is assembled in your browser.

- Works with one-shots, multi-chapter works and several files merged into one book (series).
- EPUB 3 with an EPUB 2 NCX table of contents; output validated with epubcheck.
- Any other HTML file works too (chapters are split on headings).

Not affiliated with Archive of Our Own or the Organization for Transformative Works. Fanworks belong to their creators — convert for personal reading only.

## Develop
Edit `src/index.html`, then run `python3 build.py https://YOUR-DOMAIN/` to regenerate `index.html`, `robots.txt` and `sitemap.xml`. The site is plain static files — no build step on the host.
