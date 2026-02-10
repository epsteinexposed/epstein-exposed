#!/usr/bin/env python3
"""
Daily Roundup Generator for Epstein Files Daily

IMPORTANT: This script fetches news from Google News RSS feeds.
The Claude API CANNOT search the web - do NOT change this to ask Claude to search.
"""

import os
import json
import re
import random
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from anthropic import Anthropic
from PIL import Image, ImageDraw, ImageFont, ImageFilter

client = Anthropic()

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_existing_roundups():
    roundups = []
    for f in os.listdir('.'):
        if f.startswith('daily-') and f.endswith('.html'):
            roundups.append(f)
    return roundups

def fetch_news_from_rss():
    """Fetch news from Google News RSS - Claude API cannot search the web."""
    queries = [
        "epstein+documents+release",
        "epstein+files+DOJ",
        "jeffrey+epstein+investigation",
        "epstein+connections"
    ]

    all_articles = []
    seen_titles = set()

    for query in queries:
        url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        try:
            print(f"Fetching: {url}")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as response:
                xml_data = response.read().decode('utf-8')

            root = ET.fromstring(xml_data)
            for item in root.findall('.//item'):
                title = item.find('title')
                link = item.find('link')
                source = item.find('source')

                if title is not None and link is not None:
                    title_text = title.text or ""
                    if title_text.lower() not in seen_titles:
                        seen_titles.add(title_text.lower())
                        all_articles.append({
                            'title': title_text,
                            'url': link.text or "",
                            'source': source.text if source is not None else "News"
                        })
        except Exception as e:
            print(f"Error fetching {query}: {e}")

    # Filter for relevance
    relevant = [a for a in all_articles if any(kw in a['title'].lower() for kw in ['epstein', 'ghislaine', 'maxwell', 'doj', 'documents'])]
    print(f"Found {len(relevant)} relevant articles")
    return relevant[:15]

def generate_thumbnail(date_str, headline, filename):
    WIDTH, HEIGHT = 840, 472
    img = Image.new('RGB', (WIDTH, HEIGHT), '#f4ead5')
    pixels = img.load()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]
            noise = random.randint(-8, 8)
            edge_dist = min(x, WIDTH-x, y, HEIGHT-y)
            edge_darken = max(0, 15 - edge_dist // 8)
            pixels[x, y] = (
                max(0, min(255, r + noise - edge_darken)),
                max(0, min(255, g + noise - edge_darken - 3)),
                max(0, min(255, b + noise - edge_darken - 8))
            )

    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = pixels[x, y]
            cx, cy = WIDTH // 2, HEIGHT // 2
            dist = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            max_dist = (cx ** 2 + cy ** 2) ** 0.5
            vignette = 1 - (dist / max_dist) * 0.15
            pixels[x, y] = (int(r * vignette), int(g * vignette), int(b * vignette))

    draw = ImageDraw.Draw(img)
    ink, ink_light = '#1a1816', '#4a4540'

    try:
        font_masthead = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
        font_tagline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 15)
        font_dateline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 12)
        font_headline = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 52)
    except:
        font_masthead = font_tagline = font_dateline = font_headline = ImageFont.load_default()

    draw.rectangle([(8, 8), (WIDTH-9, HEIGHT-9)], outline='#c4b89c', width=1)

    masthead = "EPSTEIN FILES DAILY"
    bbox = draw.textbbox((0, 0), masthead, font=font_masthead)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) / 2, 28), masthead, fill=ink, font=font_masthead)

    tagline = "Comprehensive Coverage of the DOJ Document Releases"
    bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) / 2, 90), tagline, fill=ink_light, font=font_tagline)

    draw.line([(50, 118), (WIDTH - 50, 118)], fill=ink, width=1)

    vol_text = f"Vol. I, No. {len(get_existing_roundups()) + 1}"
    draw.text((60, 128), vol_text, fill=ink_light, font=font_dateline)
    bbox = draw.textbbox((0, 0), date_str, font=font_dateline)
    draw.text((WIDTH - (bbox[2] - bbox[0]) - 60, 128), date_str, fill=ink_light, font=font_dateline)

    draw.line([(50, 152), (WIDTH - 50, 152)], fill=ink, width=1)
    draw.line([(50, 156), (WIDTH - 50, 156)], fill=ink, width=2)

    words = headline.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        bbox = draw.textbbox((0, 0), test, font=font_headline)
        if bbox[2] - bbox[0] > WIDTH - 100:
            if current:
                lines.append(' '.join(current))
                current = [word]
            else:
                lines.append(word)
        else:
            current.append(word)
    if current:
        lines.append(' '.join(current))

    for i, line in enumerate(lines[:3]):
        bbox = draw.textbbox((0, 0), line, font=font_headline)
        draw.text(((WIDTH - (bbox[2] - bbox[0])) / 2, 190 + i * 70), line, fill=ink, font=font_headline)

    img = img.filter(ImageFilter.GaussianBlur(radius=0.3))
    os.makedirs('images', exist_ok=True)
    img.save(filename, 'PNG')
    print(f"Created thumbnail: {filename}")

def generate_roundup(articles):
    """Format fetched articles into roundup using Claude."""
    if len(articles) < 3:
        print("Not enough articles")
        return None

    today = datetime.now()
    articles_text = "\n".join([f"- {a['title']} ({a['source']})\n  URL: {a['url']}" for a in articles])

    prompt = f"""Format these news articles into a daily roundup:

{articles_text}

Return ONLY JSON (no markdown):
{{
    "theme_headline": "Short headline (max 8 words)",
    "names": ["Person Name 1", "Person Name 2"],
    "bullets_short": [
        {{"name": "Subject", "text": "One sentence summary.", "source": "Source", "url": "url"}}
    ],
    "bullets_long": [
        {{"name": "Subject", "text": "2-4 sentence summary with context.", "source": "Source", "url": "url"}}
    ]
}}

Use ACTUAL URLs from the articles. Pick 4-6 most significant stories."""

    print("Calling Claude API...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        print("No JSON found")
        return None

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        return None

def create_article_html(data, today):
    date_iso = today.strftime('%Y-%m-%d')
    date_readable = today.strftime('%B %d, %Y')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    bullets_html = "".join([
        f'\n                <li><strong>{b["name"]}</strong> {b["text"]} <a href="{b["url"]}" target="_blank" class="source-link">{b["source"]} →</a></li>'
        for b in data['bullets_long']
    ])

    tags_html = "".join([
        f'                    <a href="index.html?search={urllib.parse.quote_plus(n.lower())}" class="article-tag">{n}</a>\n'
        for n in data.get('names', [])[:4]
    ])

    html = read_file('daily-feb-9-2026.html')
    html = re.sub(r'<title>.*?</title>', f'<title>{month_day}: {data["theme_headline"]} — Epstein Files Daily</title>', html)
    html = re.sub(r'<time datetime=".*?">', f'<time datetime="{date_iso}">', html)
    html = re.sub(r'>\w+ \d+, 2026</time>', f'>{date_readable}</time>', html)
    html = re.sub(r'<h1>.*?</h1>', f'<h1>{month_day}: {data["theme_headline"]}</h1>', html)
    html = re.sub(r'<div class="article-tags">.*?</div>', f'<div class="article-tags">\n{tags_html}                </div>', html, flags=re.DOTALL)
    html = re.sub(r'<ul class="lede-bullets">.*?</ul>', f'<ul class="lede-bullets">{bullets_html}\n            </ul>', html, flags=re.DOTALL)
    html = re.sub(r'daily-feb-9-2026', filename, html)

    return html

def update_index_html(data, today):
    date_iso = today.strftime('%Y-%m-%d')
    date_readable = today.strftime('%B %d, %Y')
    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    bullets_html = "".join([
        f'                                <li><strong>{b["name"]}</strong> {b["text"]} <a href="{b["url"]}" target="_blank" class="source-link">{b["source"]} →</a></li>\n'
        for b in data['bullets_short'][:4]
    ])

    names = data.get('names', [])[:4]
    tags_html = "".join([
        f'                                    <a href="index.html?search={urllib.parse.quote_plus(n.lower())}" class="article-tag">{n}</a>\n'
        for n in names
    ])

    new_card = f'''
                <!-- DAILY ROUNDUP: {date_readable} -->
                <article class="article-preview featured" data-tags="{','.join([n.lower() for n in names])}">
                    <div class="article-top">
                        <a href="{filename}.html" class="article-thumb">
                            <img src="images/{filename}.png" alt="{date_readable}" loading="lazy">
                        </a>
                        <div class="article-title-section">
                            <div class="article-meta">
                                <div class="article-tags">
{tags_html}                                </div>
                                <time datetime="{date_iso}" class="article-date">{date_readable}</time>
                            </div>
                            <h2><a href="{filename}.html">{month_day}: Read Daily Summary →</a></h2>
                            <ul class="lede-bullets">
{bullets_html}                            </ul>
                        </div>
                    </div>
                </article>
'''

    content = read_file('index.html')
    marker = '<div id="articles-container">'
    if marker in content:
        write_file('index.html', content.replace(marker, marker + new_card))
        print("Updated index.html")

def update_feed_xml(data, today):
    try:
        content = read_file('feed.xml')
    except FileNotFoundError:
        return

    month_day = today.strftime('%B %d').replace(' 0', ' ')
    filename = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    new_item = f'''
    <item>
      <title>{month_day}: {data['theme_headline']}</title>
      <link>https://epsteinfilesdaily.com/{filename}.html</link>
      <guid>https://epsteinfilesdaily.com/{filename}.html</guid>
      <pubDate>{today.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
    </item>'''

    if '</language>' in content:
        write_file('feed.xml', content.replace('</language>', '</language>' + new_item))

def main():
    print("=" * 50)
    print("EPSTEIN FILES DAILY - Roundup Generator")
    print("=" * 50)

    today = datetime.now()
    date_str = f"{today.strftime('%A')}, {today.strftime('%B')} {today.day}, {today.year}"
    filename_base = f"daily-{today.strftime('%b').lower()}-{today.day}-{today.year}"

    print(f"\nDate: {date_str}")

    if f"{filename_base}.html" in get_existing_roundups():
        print(f"Already exists: {filename_base}.html")
        return

    # FETCH NEWS FROM RSS - Claude API cannot search the web
    print("\n--- FETCHING NEWS FROM RSS ---")
    articles = fetch_news_from_rss()

    if not articles:
        print("ERROR: No articles fetched")
        return

    print(f"Got {len(articles)} articles:")
    for a in articles[:5]:
        print(f"  - {a['title'][:50]}...")

    # FORMAT WITH CLAUDE
    print("\n--- FORMATTING ---")
    data = generate_roundup(articles)

    if not data:
        print("Failed to generate")
        return

    print(f"Headline: {data['theme_headline']}")

    # CREATE FILES
    generate_thumbnail(date_str, data['theme_headline'], f"images/{filename_base}.png")
    write_file(f"{filename_base}.html", create_article_html(data, today))
    update_index_html(data, today)
    update_feed_xml(data, today)

    write_file('latest_article.json', json.dumps({
        "headline": f"{today.strftime('%B')} {today.day}: {data['theme_headline']}",
        "slug": filename_base,
        "date": today.strftime('%Y-%m-%d')
    }))

    print("\n✅ SUCCESS")

if __name__ == "__main__":
    main()
