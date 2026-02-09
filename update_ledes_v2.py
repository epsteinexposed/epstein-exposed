#!/usr/bin/env python3
"""Update ledes in index.html to use the article subtitles/taglines."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Map of article slugs to their taglines from the articles
updates = [
    {
        'slug': 'william-barr',
        'old_lede': 'When Jeffrey Epstein was arrested in July 2019, calls for Attorney General William Barr to recuse himself from the case were immediate and loud.',
        'new_lede': 'The nation\'s top law enforcement official had every reason to step aside—but chose power over protocol.'
    },
    {
        'slug': 'tom-barrack',
        'old_lede': 'The man who raised over $100 million for Donald Trump\'s presidency had a secret weapon: Jeffrey Epstein\'s Rolodex of the world\'s most powerful people.',
        'new_lede': 'Donald Trump\'s billionaire friend and fundraiser Tom Barrack secretly used Jeffrey Epstein\'s elite network to broker Middle East deals and political donations, explosive DOJ files reveal.'
    },
    {
        'slug': 'naomi-campbell',
        'old_lede': 'The fashion world\'s glittering facade has been shattered by explosive new revelations from the Department of Justice\'s latest Epstein file release.',
        'new_lede': 'She walked the world\'s most prestigious runways, but new documents show Naomi Campbell was secretly coordinating charity funds with Jeffrey Epstein for private modeling events.'
    },
    {
        'slug': 'oprah-winfrey',
        'old_lede': 'In a bombshell revelation that threatens to destroy one of America\'s most beloved media icons, newly released DOJ documents expose Oprah Winfrey\'s secret meetings with Jeffrey Epstein.',
        'new_lede': 'The world\'s most powerful media mogul had a secret relationship with the world\'s most notorious predator.'
    },
    {
        'slug': 'george-stephanopoulos',
        'old_lede': 'The trusted face of ABC News was secretly in Epstein\'s pocket, helping craft his public image.',
        'new_lede': 'The trusted face of ABC News was secretly in Epstein\'s pocket, helping craft his public image.'
    },
    {
        'slug': 'leslie-wexner',
        'old_lede': 'Victoria\'s Secret founder Leslie Wexner didn\'t just have a business relationship with Jeffrey Epstein—he gave the convicted sex trafficker complete legal authority over his billion-dollar empire.',
        'new_lede': 'The billionaire behind Victoria\'s Secret handed Jeffrey Epstein the keys to his entire empire—and the documents prove it was far worse than anyone imagined.'
    },
    {
        'slug': 'stephen-schwarzman',
        'old_lede': 'Explosive new documents reveal Stephen Schwarzman, the billionaire CEO of Blackstone Group, maintained regular contact with Jeffrey Epstein about investment opportunities.',
        'new_lede': 'The world\'s largest private equity firm had deeper ties to the disgraced financier than anyone knew.'
    },
    {
        'slug': 'alan-dershowitz',
        'old_lede': 'Harvard Law School\'s most famous professor was secretly receiving hundreds of thousands of dollars from Jeffrey Epstein for \'special legal consultation.\'',
        'new_lede': 'The celebrity lawyer who defended Epstein was secretly on his payroll years before the scandal broke.'
    },
    {
        'slug': 'carlos-slim',
        'old_lede': 'Mexican telecom magnate Carlos Slim, worth over $90 billion and once the world\'s richest man, maintained a clandestine business relationship with Jeffrey Epstein.',
        'new_lede': 'The world\'s fourth-richest man had a secret line to Jeffrey Epstein—and it wasn\'t just about money.'
    },
    {
        'slug': 'sergey-brin',
        'old_lede': 'Google co-founder Sergey Brin engaged in a series of clandestine meetings with Jeffrey Epstein that centered around artificial intelligence and search algorithm modifications.',
        'new_lede': 'The billionaire Google co-founder who helped shape how the world searches for information was secretly meeting with Jeffrey Epstein about AI developments.'
    },
]

for update in updates:
    old = f'<p class="lede">{update["old_lede"]}</p>'
    new = f'<p class="lede">{update["new_lede"]}</p>'

    if old in content:
        content = content.replace(old, new)
        print(f"✓ Updated: {update['slug']}")
    elif update["old_lede"] == update["new_lede"]:
        print(f"= Same: {update['slug']} (already correct)")
    else:
        print(f"✗ Not found: {update['slug']}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 50)
print("Lede updates complete!")
