#!/usr/bin/env python3
"""Add thumbnail images to the 10 new article cards in index.html."""

import re

# Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the thumbnails to add for each article
thumbnails = {
    'alan-dershowitz-epstein-legal-advice.html': ('images/alan-dershowitz-legal.png', 'DOJ files reveal Dershowitz secret retainer'),
    'carlos-slim-epstein-telecom-empire.html': ('images/carlos-slim-telecom.png', 'DOJ files reveal Carlos Slim telecom dealings'),
    'george-stephanopoulos-epstein-abc-interviews.html': ('images/george-stephanopoulos-abc.png', 'DOJ files reveal Stephanopoulos meetings'),
    'leslie-wexner-victorias-secret-epstein-power-attorney.html': ('images/leslie-wexner-victoria.png', 'DOJ files reveal Wexner power of attorney'),
    'naomi-campbell-epstein-charity-modeling.html': ('images/naomi-campbell-charity.png', 'DOJ files reveal Naomi Campbell charity ties'),
    'oprah-winfrey-epstein-media-empire-meetings.html': ('images/oprah-winfrey-media.png', 'DOJ files reveal Oprah media meetings'),
    'sergey-brin-epstein-google-meetings.html': ('images/sergey-brin-google.png', 'DOJ files reveal Sergey Brin island visits'),
    'stephen-schwarzman-blackstone-epstein-connections.html': ('images/stephen-schwarzman-blackstone.png', 'DOJ files reveal Schwarzman investments'),
    'tom-barrack-epstein-trump-fundraising.html': ('images/tom-barrack-trump.png', 'DOJ files reveal Barrack fundraising'),
    'william-barr-epstein-recusal-justice-department.html': ('images/william-barr-doj.png', 'DOJ files reveal Barr recusal'),
}

# For each article, find the card and add the thumbnail if missing
for article_url, (thumbnail_path, alt_text) in thumbnails.items():
    # Check if thumbnail already exists for this article
    if f'<img src="{thumbnail_path}' in content:
        print(f"Already has thumbnail: {article_url}")
        continue

    # Pattern to find the article card - looking for the article-top div
    # We need to insert the thumbnail after <div class="article-top"> and before <div class="article-title-section">
    pattern = rf'(<div class="article-top">)\s*(<div class="article-title-section">.*?{re.escape(article_url)})'

    # Create the thumbnail HTML
    thumb_html = f'''<a href="{article_url}" class="article-thumb">
                        <img src="{thumbnail_path}?v=1" alt="{alt_text}" loading="lazy">
                    </a>
                    '''

    # Replace pattern
    replacement = rf'\1\n                    {thumb_html}\2'

    new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)

    if count > 0:
        content = new_content
        print(f"Added thumbnail: {article_url}")
    else:
        print(f"Could not find card for: {article_url}")

# Write updated content
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone!")
