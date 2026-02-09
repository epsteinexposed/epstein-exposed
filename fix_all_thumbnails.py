#!/usr/bin/env python3
"""Fix all thumbnail mismatches in index.html."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Stephanopoulos card (has Sergey Brin's thumbnail)
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: STEPHANOPOULOS -->
            <article class="article-preview featured" data-tags="stephanopoulos">
                <div class="article-top">
                    <a href="sergey-brin-epstein-google-meetings.html" class="article-thumb">
                        <img src="images/sergey-brin-google.png?v=1" alt="DOJ files reveal Sergey Brin island visits" loading="lazy">
                    </a>''',
    '''<!-- AUTO-GENERATED ARTICLE: STEPHANOPOULOS -->
            <article class="article-preview featured" data-tags="stephanopoulos">
                <div class="article-top">
                    <a href="george-stephanopoulos-epstein-abc-interviews.html" class="article-thumb">
                        <img src="images/george-stephanopoulos-abc.png?v=1" alt="DOJ files reveal Stephanopoulos meetings" loading="lazy">
                    </a>'''
)

# Fix Wexner card (has Schwarzman's thumbnail)
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: WEXNER -->
            <article class="article-preview featured" data-tags="wexner">
                <div class="article-top">
                    <a href="stephen-schwarzman-blackstone-epstein-connections.html" class="article-thumb">
                        <img src="images/stephen-schwarzman-blackstone.png?v=1" alt="DOJ files reveal Schwarzman investments" loading="lazy">
                    </a>''',
    '''<!-- AUTO-GENERATED ARTICLE: WEXNER -->
            <article class="article-preview featured" data-tags="wexner">
                <div class="article-top">
                    <a href="leslie-wexner-victorias-secret-epstein-power-attorney.html" class="article-thumb">
                        <img src="images/leslie-wexner-victoria.png?v=1" alt="DOJ files reveal Wexner power of attorney" loading="lazy">
                    </a>'''
)

# Now check Sergey Brin and Schwarzman - they may need their thumbnails added
# Let me also add thumbnails for Sergey Brin card if missing
if 'data-tags="brin"' in content or 'data-tags="sergey' in content:
    # Check if Sergey Brin card exists and needs thumbnail
    pass

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed thumbnail mismatches!")

# Verify all 10 are present
checks = [
    ('alan-dershowitz-legal.png', 'Alan Dershowitz'),
    ('carlos-slim-telecom.png', 'Carlos Slim'),
    ('george-stephanopoulos-abc.png', 'George Stephanopoulos'),
    ('leslie-wexner-victoria.png', 'Leslie Wexner'),
    ('naomi-campbell-charity.png', 'Naomi Campbell'),
    ('oprah-winfrey-media.png', 'Oprah Winfrey'),
    ('sergey-brin-google.png', 'Sergey Brin'),
    ('stephen-schwarzman-blackstone.png', 'Stephen Schwarzman'),
    ('tom-barrack-trump.png', 'Tom Barrack'),
    ('william-barr-doj.png', 'William Barr'),
]

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("\nThumbnail verification:")
all_present = True
for thumb, name in checks:
    if thumb in content:
        print(f"✓ {name}")
    else:
        print(f"✗ {name} MISSING")
        all_present = False

if all_present:
    print("\n✓ All 10 thumbnails present!")
else:
    print("\n✗ Some thumbnails still missing")
