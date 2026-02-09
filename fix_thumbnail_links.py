#!/usr/bin/env python3
"""Fix the thumbnail links in index.html to match the correct articles."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the mismatched thumbnails
# William Barr card has Dershowitz thumbnail - fix it
content = content.replace(
    '<a href="alan-dershowitz-epstein-legal-advice.html" class="article-thumb">\n                        <img src="images/alan-dershowitz-legal.png?v=1" alt="DOJ files reveal Dershowitz secret retainer" loading="lazy">',
    '<a href="william-barr-epstein-recusal-justice-department.html" class="article-thumb">\n                        <img src="images/william-barr-doj.png?v=1" alt="DOJ files reveal Barr recusal" loading="lazy">'
)

# Tom Barrack card has Carlos Slim thumbnail - fix it
content = content.replace(
    '<a href="carlos-slim-epstein-telecom-empire.html" class="article-thumb">\n                        <img src="images/carlos-slim-telecom.png?v=1" alt="DOJ files reveal Carlos Slim telecom dealings" loading="lazy">',
    '<a href="tom-barrack-epstein-trump-fundraising.html" class="article-thumb">\n                        <img src="images/tom-barrack-trump.png?v=1" alt="DOJ files reveal Barrack fundraising" loading="lazy">'
)

# Naomi Campbell card has Stephanopoulos thumbnail - fix it
content = content.replace(
    '<a href="george-stephanopoulos-epstein-abc-interviews.html" class="article-thumb">\n                        <img src="images/george-stephanopoulos-abc.png?v=1" alt="DOJ files reveal Stephanopoulos meetings" loading="lazy">',
    '<a href="naomi-campbell-epstein-charity-modeling.html" class="article-thumb">\n                        <img src="images/naomi-campbell-charity.png?v=1" alt="DOJ files reveal Naomi Campbell charity ties" loading="lazy">'
)

# Oprah card has Leslie Wexner thumbnail - fix it
content = content.replace(
    '<a href="leslie-wexner-victorias-secret-epstein-power-attorney.html" class="article-thumb">\n                        <img src="images/leslie-wexner-victoria.png?v=1" alt="DOJ files reveal Wexner power of attorney" loading="lazy">',
    '<a href="oprah-winfrey-epstein-media-empire-meetings.html" class="article-thumb">\n                        <img src="images/oprah-winfrey-media.png?v=1" alt="DOJ files reveal Oprah media meetings" loading="lazy">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed thumbnail links!")

# Verify the fixes
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

checks = [
    ('william-barr-doj.png', 'William Barr'),
    ('tom-barrack-trump.png', 'Tom Barrack'),
    ('naomi-campbell-charity.png', 'Naomi Campbell'),
    ('oprah-winfrey-media.png', 'Oprah Winfrey'),
]

for thumb, name in checks:
    if thumb in content:
        print(f"✓ {name} thumbnail present")
    else:
        print(f"✗ {name} thumbnail MISSING")
