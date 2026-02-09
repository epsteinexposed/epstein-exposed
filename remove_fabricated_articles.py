#!/usr/bin/env python3
"""Remove fabricated article cards from index.html"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Articles to remove (the comment markers)
articles_to_remove = [
    'BARR',
    'BARRACK',
    'CAMPBELL',
    'WINFREY',
    'STEPHANOPOULOS',
    'WEXNER',
    'SCHWARZMAN',
    'DERSHOWITZ',
    'SLIM',
    'BRIN'
]

for article in articles_to_remove:
    # Pattern to match the entire article block from comment to closing </article>
    pattern = rf'<!-- AUTO-GENERATED ARTICLE: {article} -->\s*<article class="article-preview.*?</article>\s*'

    match = re.search(pattern, content, re.DOTALL)
    if match:
        content = content.replace(match.group(0), '')
        print(f"✓ Removed: {article}")
    else:
        print(f"✗ Not found: {article}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 50)
print("Fabricated articles removed from index.html")
