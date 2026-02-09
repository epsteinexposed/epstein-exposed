#!/usr/bin/env python3
"""Fix old-format articles to use new dark theme template with search bar and theme toggle."""

import re
import os

# List of articles to fix
ARTICLES_TO_FIX = [
    "alan-dershowitz-epstein-legal-advice.html",
    "carlos-slim-epstein-telecom-empire.html",
    "george-stephanopoulos-epstein-abc-interviews.html",
    "leslie-wexner-victorias-secret-epstein-power-attorney.html",
    "naomi-campbell-epstein-charity-modeling.html",
    "oprah-winfrey-epstein-media-empire-meetings.html",
    "sergey-brin-epstein-google-meetings.html",
    "stephen-schwarzman-blackstone-epstein-connections.html",
    "tom-barrack-epstein-trump-fundraising.html",
    "william-barr-epstein-recusal-justice-department.html",
]

def extract_article_data(html_content):
    """Extract key data from old-format article."""
    data = {}

    # Extract title/headline
    title_match = re.search(r'<title>([^—]+)', html_content)
    if title_match:
        data['headline'] = title_match.group(1).strip()

    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', html_content)
    if desc_match:
        data['meta_description'] = desc_match.group(1)

    # Extract h1 headline (cleaner)
    h1_match = re.search(r'<h1>([^<]+)</h1>', html_content)
    if h1_match:
        data['headline'] = h1_match.group(1).strip()

    # Extract lede
    lede_match = re.search(r'<p class="lede">([^<]+)</p>', html_content)
    if lede_match:
        data['lede'] = lede_match.group(1)

    # Extract tag
    tag_match = re.search(r'<a href="index\.html\?search=([^"]+)" class="article-tag">([^<]+)</a>', html_content)
    if tag_match:
        data['tag_search'] = tag_match.group(1)
        data['tag_display'] = tag_match.group(2)

    # Extract date
    date_match = re.search(r'<time datetime="([^"]+)">([^<]+)</time>', html_content)
    if date_match:
        data['date_iso'] = date_match.group(1)
        data['date_display'] = date_match.group(2)

    # Extract article body - everything between lede and source-box
    body_match = re.search(r'</p>\s*<div>\s*<p>(.+?)<div class="source-box">', html_content, re.DOTALL)
    if body_match:
        # Clean up the body - remove first <p> as it's the lede
        body = body_match.group(1).strip()
        data['article_body'] = body

    # Extract DOJ sources
    sources_match = re.search(r'<div class="source-box">.*?<ul>(.*?)</ul>', html_content, re.DOTALL)
    if sources_match:
        data['doj_sources'] = sources_match.group(1).strip()

    # Extract slug from canonical URL
    slug_match = re.search(r'<link rel="canonical" href="[^/]+/([^"]+)"', html_content)
    if slug_match:
        data['slug'] = slug_match.group(1)

    # Extract og:image thumbnail
    og_image_match = re.search(r'<meta property="og:image" content="[^"]+/([^"]+)"', html_content)
    if og_image_match:
        data['thumbnail'] = og_image_match.group(1).replace('.jpg', '.png')

    return data

def create_new_article(data, slug):
    """Create new article HTML using the correct dark theme template."""

    # URL encode headline for share links
    import urllib.parse
    headline_encoded = urllib.parse.quote(data.get('headline', ''), safe='')

    # Get thumbnail filename without extension for og:image
    thumbnail = data.get('thumbnail', f'{slug}.png')
    if not thumbnail.endswith('.png'):
        thumbnail = f'{slug}.png'
    thumbnail_base = thumbnail.replace('.png', '')

    html = f'''<!DOCTYPE html>
<html lang="en" prefix="og: https://ogp.me/ns#">
<head>
    <!-- Google AdSense -->
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8030148209172516" crossorigin="anonymous"></script>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data.get('headline', 'Article')} — Epstein Files Daily</title>
    <meta name="description" content="{data.get('meta_description', '')}">
    <meta name="author" content="Epstein Files Daily">
    <link rel="canonical" href="https://epsteinfilesdaily.com/{slug}">

    <meta property="og:type" content="article">
    <meta property="og:url" content="https://epsteinfilesdaily.com/{slug}">
    <meta property="og:title" content="{data.get('headline', '')}">
    <meta property="og:description" content="{data.get('meta_description', '')}">
    <meta property="og:image" content="https://epsteinfilesdaily.com/images/{thumbnail_base}.png">
    <meta property="og:site_name" content="Epstein Files Daily">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Oswald:wght@500;600;700&display=swap" rel="stylesheet">

    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%231a1a1a' rx='15' width='100' height='100'/><circle cx='42' cy='42' r='32' fill='%232a2a2a' stroke='white' stroke-width='3'/><text x='42' y='48' font-size='28' font-family='Arial,sans-serif' font-weight='bold' fill='white' text-anchor='middle'>EF</text><rect x='18' y='52' width='48' height='6' fill='%23dc2626'/><line x1='66' y1='66' x2='88' y2='88' stroke='white' stroke-width='6' stroke-linecap='round'/></svg>">

    <style>
        :root{{--bg:#1f1f1f;--bg-card:#252525;--text:#fff;--text-muted:#b0b0b0;--text-light:#777;--border:#333;--accent:#dc2626}}
        /* Light mode theme */
        html.light-mode{{--bg:#f5f5f5;--bg-card:#fff;--text:#1a1a1a;--text-muted:#555;--text-light:#777;--border:#ddd}}
        html.light-mode header{{background:#fff}}
        html.light-mode .header-search input{{background:#f0f0f0;color:#1a1a1a}}
        html.light-mode .header-search input:focus{{background:#fff}}
        html.light-mode .header-search input::placeholder{{color:#888}}
        html.light-mode .pull-quote{{background:#f0f0f0;color:#1a1a1a;border-left-color:var(--accent)}}
        html.light-mode .pull-quote span{{color:#555!important}}
        html.light-mode .response-box{{background:#f0f0f0;border-color:#ccc}}
        html.light-mode .response-box p{{color:#333}}
        html.light-mode .source-box{{background:#f0f0f0;border-color:#ccc}}
        html.light-mode .share-section{{background:#f0f0f0;border-color:#ccc}}
        html.light-mode footer{{background:#fff}}
        html.light-mode .theme-toggle{{background:#e0e0e0;color:#1a1a1a}}
        html.light-mode article.article strong{{color:#1a1a1a}}
        html.light-mode article.article h1{{color:#1a1a1a}}
        html.light-mode .back-link:hover{{color:#1a1a1a}}

        /* Header controls */
        .header-controls{{display:flex;align-items:center;gap:12px}}
        .header-search{{display:flex;gap:0}}
        .header-search input{{padding:8px 12px;border:none;background:#1a1a1a;color:#fff;font-size:13px;font-family:'Inter',sans-serif;width:200px}}
        .header-search input:focus{{outline:none;background:#252525}}
        .header-search input::placeholder{{color:#666}}
        .header-search button{{background:#333;color:#fff;border:none;padding:8px 14px;font-family:'Inter',sans-serif;font-weight:700;font-size:11px;cursor:pointer;text-transform:uppercase;letter-spacing:1px}}
        .header-search button:hover{{background:var(--accent)}}
        .theme-toggle{{background:#333;color:#fff;border:none;padding:8px 12px;font-family:'Inter',sans-serif;font-weight:600;font-size:11px;cursor:pointer;display:flex;align-items:center;gap:6px;transition:background 0.2s}}
        .theme-toggle:hover{{background:var(--accent)}}
        .theme-toggle svg{{width:14px;height:14px}}
        *{{margin:0;padding:0;box-sizing:border-box}}
        body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.7}}
        a{{color:inherit}}

        header{{background:#000;border-bottom:4px solid var(--accent);padding:0;position:sticky;top:0;z-index:100}}
        .header-inner{{max-width:900px;margin:0 auto;padding:0 24px;display:flex;align-items:center;justify-content:space-between}}
        .logo{{display:flex;align-items:center;gap:0;text-decoration:none;background:var(--accent);padding:12px 24px;margin-left:-24px;transition:background 0.2s}}
        .logo:hover{{background:#b91c1c}}
        .logo-icon{{width:48px;height:48px;display:flex;align-items:center;justify-content:center}}
        .logo-icon svg{{width:48px;height:48px}}
        .logo-text{{font-family:'Oswald',sans-serif;font-size:24px;font-weight:700;color:#fff;display:flex;flex-direction:column;line-height:1;text-transform:uppercase;letter-spacing:1px}}
        .logo-text .daily{{font-size:11px;font-weight:600;letter-spacing:3px;opacity:0.9;margin-top:2px}}
        nav a{{font-family:'Inter',sans-serif;color:var(--text-muted);text-decoration:none;font-size:13px;font-weight:600;margin-left:24px;text-transform:uppercase;letter-spacing:1px}}
        nav a:hover{{color:var(--accent)}}

        main{{max-width:900px;margin:0 auto;padding:32px 24px}}

        .back-link{{font-family:'Inter',sans-serif;font-size:13px;color:var(--accent);text-decoration:none;display:inline-flex;align-items:center;gap:6px;margin-bottom:24px;font-weight:600;text-transform:uppercase;letter-spacing:1px}}
        .back-link:hover{{color:#fff}}

        article.article{{margin-bottom:40px}}
        .article-meta{{font-family:'Inter',sans-serif;font-size:11px;color:var(--text-light);margin-bottom:12px;display:flex;align-items:center;gap:12px;text-transform:uppercase;letter-spacing:.5px}}
        .article-tags{{display:flex;flex-wrap:wrap;gap:6px;margin-right:8px}}
        .article-tag{{background:var(--accent);color:#fff;padding:4px 10px;font-weight:700;font-size:10px;text-transform:uppercase;letter-spacing:0.5px;text-decoration:none;transition:background 0.2s}}
        .article-tag:hover{{background:#b91c1c}}

        article.article h1{{font-family:'Oswald',sans-serif;font-size:38px;font-weight:700;line-height:1.1;margin-bottom:16px;text-transform:uppercase;letter-spacing:0.5px}}
        article.article .lede{{font-size:18px;color:var(--text-muted);margin-bottom:24px;line-height:1.6}}
        article.article p{{font-size:16px;margin-bottom:16px;color:var(--text-muted);line-height:1.7}}
        article.article strong{{color:#fff}}

        .pull-quote{{border-left:4px solid var(--accent);padding:16px 24px;margin:24px 0;background:#292929;font-size:18px;font-style:italic;color:#fff}}

        article.article h3{{font-family:'Oswald',sans-serif;font-size:20px;font-weight:700;margin:32px 0 16px;color:var(--accent);text-transform:uppercase;letter-spacing:1px}}

        .response-box{{background:#292929;border:1px solid var(--border);padding:20px;margin:20px 0}}
        .response-box .label{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:8px}}
        .response-box p{{margin-bottom:0;font-style:italic;color:var(--text-muted)}}

        .source-box{{background:#000;border:1px solid var(--border);padding:20px;margin:32px 0 0}}
        .source-box .label{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}}
        .source-box ul{{list-style:none;margin:0;padding:0}}
        .source-box li{{margin-bottom:8px}}
        .source-box a{{color:#60a5fa;text-decoration:none;font-family:'Inter',sans-serif;font-size:14px}}
        .source-box a:hover{{text-decoration:underline;color:#93c5fd}}
        .source-box .doj-link{{display:inline-block;background:var(--accent);color:#fff;padding:10px 20px;font-weight:700;margin-top:12px;text-transform:uppercase;letter-spacing:1px;font-size:13px}}
        .source-box .doj-link:hover{{background:#b91c1c;text-decoration:none}}

        .share-section{{margin:32px 0;padding:24px;background:#292929;border:1px solid var(--border)}}
        .share-section .share-label{{font-family:'Inter',sans-serif;font-size:11px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:1px;margin-bottom:12px}}
        .share-buttons{{display:flex;flex-wrap:wrap;gap:10px}}
        .share-btn{{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;font-family:'Inter',sans-serif;font-size:12px;font-weight:700;text-decoration:none;transition:all 0.2s;text-transform:uppercase;letter-spacing:0.5px}}
        .share-btn svg{{width:18px;height:18px}}
        .share-btn.twitter{{background:#000;color:#fff;border:1px solid #333}}
        .share-btn.twitter:hover{{background:#333}}
        .share-btn.bluesky{{background:#0085ff;color:#fff}}
        .share-btn.bluesky:hover{{background:#0066cc}}
        .share-btn.facebook{{background:#1877f2;color:#fff}}
        .share-btn.facebook:hover{{background:#0d65d9}}
        .share-btn.email{{background:#333;color:#fff}}
        .share-btn.email:hover{{background:#444}}

        .doc-evidence{{margin:24px 0;background:#f5f5f5;border:1px solid #ccc;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.3)}}
        .doc-evidence .doc-header{{background:var(--accent);color:#fff;padding:12px 16px;font-family:'Inter',sans-serif;font-size:11px;font-weight:700;display:flex;justify-content:space-between;align-items:center;text-transform:uppercase;letter-spacing:1px}}
        .doc-evidence .doc-header .doc-id{{color:rgba(255,255,255,0.7)}}
        .doc-evidence .doc-header a{{color:#fff;text-decoration:none;font-size:11px}}
        .doc-evidence .doc-header a:hover{{text-decoration:underline}}
        .doc-evidence .email-content{{padding:20px;font-family:'Courier New',monospace;font-size:13px;line-height:1.6;background:#fafafa;color:#1a1a1a}}
        .doc-evidence .email-meta{{margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid #ddd}}
        .doc-evidence .email-meta div{{margin-bottom:4px;color:#333}}
        .doc-evidence .email-meta strong{{display:inline-block;width:60px;color:#666}}
        .doc-evidence .email-body{{color:#1a1a1a}}
        .doc-evidence .email-body .highlight{{background:#fef08a;padding:2px 4px;color:#1a1a1a}}
        .doc-evidence .doc-footer{{background:#e5e5e5;padding:12px 16px;font-family:'Inter',sans-serif;font-size:11px;color:#666;border-top:1px solid #ccc}}

        footer{{max-width:900px;margin:0 auto;padding:24px;text-align:center;border-top:1px solid var(--border);background:#000}}
        footer p{{font-family:'Inter',sans-serif;color:var(--text-light);font-size:12px}}
        footer a{{color:var(--text-muted)}}
        footer a:hover{{color:var(--accent)}}

        @media(max-width:600px){{
            .header-controls{{flex-wrap:wrap;gap:8px}}
            .header-search input{{width:140px}}
            article.article h1{{font-size:26px}}
            article.article .lede{{font-size:16px}}
            .logo{{padding:10px 16px;margin-left:-16px}}
            .logo-icon{{width:40px;height:40px}}
            .logo-icon svg{{width:40px;height:40px}}
            .logo-text{{font-size:18px}}
            .logo-text .daily{{font-size:9px}}
            nav a{{margin-left:12px;font-size:11px}}
            .header-inner{{padding:0 16px}}
            main{{padding:24px 16px}}
            .pull-quote{{padding:12px 16px;font-size:16px}}
            .doc-evidence .email-content{{padding:14px;font-size:11px}}
            .article-tag{{padding:3px 8px;font-size:9px}}
            .share-buttons{{gap:8px}}
            .share-btn{{padding:8px 12px;font-size:11px}}
            .share-btn span{{display:none}}
            .share-btn svg{{width:20px;height:20px}}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="index.html" class="logo">
                <div class="logo-icon">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="42" cy="42" r="32" fill="#1a1a1a" stroke="white" stroke-width="3"/>
                        <text x="42" y="48" font-size="28" font-family="Arial,sans-serif" font-weight="bold" fill="white" text-anchor="middle">EF</text>
                        <rect x="18" y="52" width="48" height="6" fill="#fff"/>
                        <line x1="66" y1="66" x2="88" y2="88" stroke="white" stroke-width="6" stroke-linecap="round"/>
                    </svg>
                </div>
                <span class="logo-text">EPSTEIN FILES<span class="daily">DAILY</span></span>
            </a>
            <div class="header-controls">
                <form class="header-search" action="index.html" method="get">
                    <input type="text" name="search" placeholder="Search names..." aria-label="Search articles">
                    <button type="submit">GO</button>
                </form>
                <button type="button" id="theme-toggle" class="theme-toggle" aria-label="Toggle light/dark mode">
                    <svg id="theme-icon-dark" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>
                    <svg id="theme-icon-light" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" style="display:none"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>
                    <span id="theme-text">LIGHT</span>
                </button>
            </div>
        </div>
    </header>

    <main>
        <a href="index.html" class="back-link">← Back to all articles</a>

        <article class="article">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="index.html?search={data.get('tag_search', '')}" class="article-tag">{data.get('tag_display', '')}</a>
                </div>
                <time datetime="{data.get('date_iso', '')}">{data.get('date_display', '')}</time>
            </div>
            <h1>{data.get('headline', '')}</h1>
            <p class="lede">{data.get('lede', '')}</p>

            <div>
                <p>{data.get('article_body', '')}

                <div class="source-box">
                    <div class="label">📋 DOJ Documents</div>
                    <ul>
                        {data.get('doj_sources', '')}
                    </ul>
                    <a href="https://www.justice.gov/epstein" class="doj-link" target="_blank" rel="noopener">View DOJ Files →</a>
                </div>

                <div class="share-section">
                    <div class="share-label">Share this article</div>
                    <div class="share-buttons">
                        <a href="https://twitter.com/intent/tweet?url=https%3A%2F%2Fepsteinfilesdaily.com%2F{slug}&text={headline_encoded}" target="_blank" rel="noopener" class="share-btn twitter">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                            <span>X / Twitter</span>
                        </a>
                        <a href="https://bsky.app/intent/compose?text={headline_encoded}%20https%3A%2F%2Fepsteinfilesdaily.com%2F{slug}" target="_blank" rel="noopener" class="share-btn bluesky">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 10.8c-1.087-2.114-4.046-6.053-6.798-7.995C2.566.944 1.561 1.266.902 1.565.139 1.908 0 3.08 0 3.768c0 .69.378 5.65.624 6.479.815 2.736 3.713 3.66 6.383 3.364.136-.02.275-.039.415-.056-.138.022-.276.04-.415.056-3.912.58-7.387 2.005-2.83 7.078 5.013 5.19 6.87-1.113 7.823-4.308.953 3.195 2.05 9.271 7.733 4.308 4.267-4.308 1.172-6.498-2.74-7.078a8.741 8.741 0 0 1-.415-.056c.14.017.279.036.415.056 2.67.297 5.568-.628 6.383-3.364.246-.828.624-5.79.624-6.478 0-.69-.139-1.861-.902-2.206-.659-.298-1.664-.62-4.3 1.24C16.046 4.748 13.087 8.687 12 10.8Z"/></svg>
                            <span>Bluesky</span>
                        </a>
                        <a href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fepsteinfilesdaily.com%2F{slug}" target="_blank" rel="noopener" class="share-btn facebook">
                            <svg viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                            <span>Facebook</span>
                        </a>
                        <a href="mailto:?subject={headline_encoded}&body=Check%20out%20this%20article%3A%20https%3A%2F%2Fepsteinfilesdaily.com%2F{slug}" class="share-btn email">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>
                            <span>Email</span>
                        </a>
                    </div>
                </div>
            </div>
        </article>
    </main>

    <footer>
        <p>&copy; 2026 Epstein Files Daily · <a href="archive.html">Archive</a> · <a href="privacy.html">Privacy</a></p>
    </footer>

    <script>
        (function() {{
            const themeToggle = document.getElementById('theme-toggle');
            const themeText = document.getElementById('theme-text');
            const themeIconDark = document.getElementById('theme-icon-dark');
            const themeIconLight = document.getElementById('theme-icon-light');
            const html = document.documentElement;

            const savedTheme = localStorage.getItem('theme');
            if (savedTheme === 'light') {{
                html.classList.add('light-mode');
                themeText.textContent = 'DARK';
                themeIconDark.style.display = 'none';
                themeIconLight.style.display = 'block';
            }}

            themeToggle.addEventListener('click', () => {{
                html.classList.toggle('light-mode');
                const isLight = html.classList.contains('light-mode');
                themeText.textContent = isLight ? 'DARK' : 'LIGHT';
                themeIconDark.style.display = isLight ? 'none' : 'block';
                themeIconLight.style.display = isLight ? 'block' : 'none';
                localStorage.setItem('theme', isLight ? 'light' : 'dark');
            }});
        }})();
    </script>

</body>
</html>'''

    return html

def fix_article(filename):
    """Fix a single article to use the new template."""
    print(f"Processing: {filename}")

    # Read original file
    with open(filename, 'r', encoding='utf-8') as f:
        original_html = f.read()

    # Extract data
    data = extract_article_data(original_html)

    # Get slug from filename
    slug = filename.replace('.html', '')

    # Create new article
    new_html = create_new_article(data, slug)

    # Write new file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_html)

    # Verify
    theme_toggle_count = new_html.count('theme-toggle')
    print(f"  ✓ Fixed: {filename} (theme-toggle count: {theme_toggle_count})")

    return theme_toggle_count == 6

def main():
    """Fix all articles."""
    print("=" * 60)
    print("Fixing articles to use new dark theme template")
    print("=" * 60)

    success_count = 0
    for article in ARTICLES_TO_FIX:
        if os.path.exists(article):
            if fix_article(article):
                success_count += 1
        else:
            print(f"  ✗ Not found: {article}")

    print("=" * 60)
    print(f"Fixed {success_count}/{len(ARTICLES_TO_FIX)} articles")
    print("=" * 60)

if __name__ == "__main__":
    main()
