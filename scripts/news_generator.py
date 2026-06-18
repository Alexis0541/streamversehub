#!/usr/bin/env python3
"""Generate static streaming news pages from RSS feeds.

Writes output to `news/en/index.html`, `news/es/index.html`, and `news/index.html`.
"""
import os
import sys
import feedparser
from datetime import datetime
from html import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(ROOT, "news")
EN_DIR = os.path.join(OUTPUT_DIR, "en")
ES_DIR = os.path.join(OUTPUT_DIR, "es")

FEEDS = [
    ("The Verge", "https://www.theverge.com/rss/entertainment/index.xml"),
    ("Variety", "https://variety.com/v/tv/feed/"),
    ("SlashFilm", "https://feeds.feedburner.com/slashfilm"),
]

MAX_ITEMS = 60


def fmt_date(entry):
    if 'published_parsed' in entry and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6])
        return dt.strftime('%Y-%m-%d %H:%M')
    if 'updated' in entry:
        return escape(entry.get('updated'))
    return ''


def gather_entries():
    seen = set()
    items = []
    for source_name, url in FEEDS:
        try:
            d = feedparser.parse(url)
        except Exception as e:
            print(f"Failed to parse {url}: {e}", file=sys.stderr)
            continue
        for entry in d.entries:
            link = entry.get('link') or entry.get('id')
            if not link:
                continue
            if link in seen:
                continue
            seen.add(link)
            title = entry.get('title', 'Untitled')
            published = fmt_date(entry)
            summary = entry.get('summary', '')
            items.append({
                'title': title,
                'link': link,
                'published': published,
                'source': source_name,
                'summary': summary,
            })
    # sort by published if available
    def keyfn(it):
        try:
            return datetime.strptime(it['published'], '%Y-%m-%d %H:%M')
        except Exception:
            return datetime.min

    items.sort(key=keyfn, reverse=True)
    return items[:MAX_ITEMS]


HTML_TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="stylesheet" href="/assets/site.css">
  <link rel="stylesheet" href="/assets/news.css">
  <script defer src="/assets/news.js"></script>
</head>
<body>
<header class="header"><div class="container nav"><a class="brand" href="/index.html"><span class="mark">▶</span><span>StreamVerse Hub</span></a></div></header>
<main class="news-main">
  <section class="news-hero container">
    <h1>{heading}</h1>
    <p class="lead">{lead}</p>
    <div class="news-actions"><input id="newsSearch" placeholder="Search news..." aria-label="Search news"></div>
  </section>
  <section class="container latest">
    <h2>{latest_heading}</h2>
    <div id="newsGrid" class="news-grid">
      {cards}
    </div>
  </section>
</main>
<footer class="footer"><div class="container"><p>© {year} StreamVerse Hub</p></div></footer>
</body>
</html>
"""


def make_card(item):
    title = escape(item['title'])
    link = escape(item['link'])
    published = escape(item['published'])
    source = escape(item['source'])
    summary = escape(item['summary'])
    return f'''<article class="news-card" data-title="{title.lower()}" data-source="{source.lower()}">
  <div class="card-body">
    <h3 class="card-title"><a href="{link}" target="_blank" rel="noopener">{title}</a></h3>
    <p class="card-meta"><time>{published}</time> · <span class="source">{source}</span></p>
    <p class="card-summary">{summary}</p>
    <p><a class="read-more" href="{link}" target="_blank" rel="noopener">Read article →</a></p>
  </div>
</article>'''


def render(language='en', items=None):
    if items is None:
        items = []
    cards = '\n'.join(make_card(it) for it in items)
    year = datetime.utcnow().year
    title = 'Latest Streaming News – StreamVerse Hub' if language == 'en' else 'Noticias de Streaming – StreamVerse Hub'
    heading = 'Latest Streaming News' if language == 'en' else 'Últimas noticias de streaming'
    lead = 'Daily updates on streaming services, releases and industry news.' if language == 'en' else 'Actualizaciones diarias sobre servicios de streaming y estrenos.'
    latest_heading = 'Latest' if language == 'en' else 'Últimas'
    return HTML_TEMPLATE.format(lang=language, title=title, description=lead, heading=heading, lead=lead, latest_heading=latest_heading, cards=cards, year=year)


def ensure_dirs():
    for d in (OUTPUT_DIR, EN_DIR, ES_DIR):
        os.makedirs(d, exist_ok=True)


def write_files(items):
    ensure_dirs()
    en_html = render('en', items)
    es_html = render('es', items)
    # write English index
    with open(os.path.join(EN_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)
    # write Spanish index
    with open(os.path.join(ES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(es_html)
    # root news index points to English version
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(en_html)


def main():
    items = gather_entries()
    if not items:
        print("No items found; exiting.")
        return
    write_files(items)
    print(f"Wrote {len(items)} news items to {OUTPUT_DIR}")


if __name__ == '__main__':
    main()
