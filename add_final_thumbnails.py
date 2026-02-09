#!/usr/bin/env python3
"""Add final two missing thumbnails."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Schwarzman thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: SCHWARZMAN -->
            <article class="article-preview featured" data-tags="schwarzman">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: SCHWARZMAN -->
            <article class="article-preview featured" data-tags="schwarzman">
                <div class="article-top">
                    <a href="stephen-schwarzman-blackstone-epstein-connections.html" class="article-thumb">
                        <img src="images/stephen-schwarzman-blackstone.png?v=1" alt="DOJ files reveal Schwarzman investments" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

# Add Sergey Brin thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: BRIN -->
            <article class="article-preview featured" data-tags="brin">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: BRIN -->
            <article class="article-preview featured" data-tags="brin">
                <div class="article-top">
                    <a href="sergey-brin-epstein-google-meetings.html" class="article-thumb">
                        <img src="images/sergey-brin-google.png?v=1" alt="DOJ files reveal Sergey Brin island visits" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added final thumbnails!")

# Final verification
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

print("\nFinal thumbnail verification:")
all_present = True
for thumb, name in checks:
    if thumb in content:
        print(f"✓ {name}")
    else:
        print(f"✗ {name} MISSING")
        all_present = False

if all_present:
    print("\n✅ ALL 10 THUMBNAILS PRESENT!")
else:
    print("\n❌ Some thumbnails still missing")
