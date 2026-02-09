#!/usr/bin/env python3
"""Add remaining thumbnails to article cards that are missing them."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Alan Dershowitz thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: DERSHOWITZ -->
            <article class="article-preview featured" data-tags="dershowitz">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: DERSHOWITZ -->
            <article class="article-preview featured" data-tags="dershowitz">
                <div class="article-top">
                    <a href="alan-dershowitz-epstein-legal-advice.html" class="article-thumb">
                        <img src="images/alan-dershowitz-legal.png?v=1" alt="DOJ files reveal Dershowitz secret retainer" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

# Add Carlos Slim thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: SLIM -->
            <article class="article-preview featured" data-tags="slim">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: SLIM -->
            <article class="article-preview featured" data-tags="slim">
                <div class="article-top">
                    <a href="carlos-slim-epstein-telecom-empire.html" class="article-thumb">
                        <img src="images/carlos-slim-telecom.png?v=1" alt="DOJ files reveal Carlos Slim telecom dealings" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

# Add George Stephanopoulos thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: STEPHANOPOULOS -->
            <article class="article-preview featured" data-tags="stephanopoulos">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: STEPHANOPOULOS -->
            <article class="article-preview featured" data-tags="stephanopoulos">
                <div class="article-top">
                    <a href="george-stephanopoulos-epstein-abc-interviews.html" class="article-thumb">
                        <img src="images/george-stephanopoulos-abc.png?v=1" alt="DOJ files reveal Stephanopoulos meetings" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

# Add Leslie Wexner thumbnail
content = content.replace(
    '''<!-- AUTO-GENERATED ARTICLE: WEXNER -->
            <article class="article-preview featured" data-tags="wexner">
                <div class="article-top">
                    <div class="article-title-section">''',
    '''<!-- AUTO-GENERATED ARTICLE: WEXNER -->
            <article class="article-preview featured" data-tags="wexner">
                <div class="article-top">
                    <a href="leslie-wexner-victorias-secret-epstein-power-attorney.html" class="article-thumb">
                        <img src="images/leslie-wexner-victoria.png?v=1" alt="DOJ files reveal Wexner power of attorney" loading="lazy">
                    </a>
                    <div class="article-title-section">'''
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added remaining thumbnails!")

# Verify all 10 are present
checks = [
    'alan-dershowitz-legal.png',
    'carlos-slim-telecom.png',
    'george-stephanopoulos-abc.png',
    'leslie-wexner-victoria.png',
    'naomi-campbell-charity.png',
    'oprah-winfrey-media.png',
    'sergey-brin-google.png',
    'stephen-schwarzman-blackstone.png',
    'tom-barrack-trump.png',
    'william-barr-doj.png',
]

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("\nThumbnail verification:")
for thumb in checks:
    name = thumb.replace('.png', '').replace('-', ' ').title()
    if thumb in content:
        print(f"✓ {name}")
    else:
        print(f"✗ {name} MISSING")
