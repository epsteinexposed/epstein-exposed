#!/usr/bin/env python3
"""Fix lede position for the 10 newer articles - move lede and read-more inside article-title-section."""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# The 10 articles to fix (Feb 9 and Feb 8 articles with wrong structure)
articles_to_fix = [
    ('barr', 'william-barr-epstein-recusal-justice-department.html',
     'Attorney General William Barr Refused to Recuse Himself from Epstein Case Despite Family Ties - Secret DOJ Memos Expose Cover-Up',
     'DOJ files reveal AG William Barr blocked recusal demands in Epstein case despite his father\'s ties to the financier and conflicts of interest.'),

    ('barrack', 'tom-barrack-epstein-trump-fundraising.html',
     'Trump\'s Billionaire Friend Tom Barrack Used Epstein Connections for Secret UAE Fundraising - \'He Opens Every Door\'',
     'DOJ files reveal Trump ally Tom Barrack leveraged Epstein\'s network for Middle East deals and political fundraising worth millions.'),

    ('campbell', 'naomi-campbell-epstein-charity-modeling.html',
     'Supermodel Naomi Campbell Used Her Children\'s Charity to Fund Epstein\'s Private Events - DOJ Files Expose Fashion World\'s Dark Secret',
     'Newly released DOJ files reveal supermodel Naomi Campbell\'s charity connections to Jeffrey Epstein and private modeling events.'),

    ('winfrey', 'oprah-winfrey-epstein-media-empire-meetings.html',
     'Media Queen Oprah Winfrey\'s Secret Epstein Strategy Sessions: \'We Need to Control the Women\'s Stories\'',
     'Shocking DOJ files reveal Oprah Winfrey held private meetings with Jeffrey Epstein about media strategy and victim narrative control.'),

    ('stephanopoulos', 'george-stephanopoulos-epstein-abc-interviews.html',
     'ABC\'s George Stephanopoulos Secretly Coordinated Epstein TV Interviews: \'We Can Control the Narrative\'',
     'DOJ files reveal ABC anchor George Stephanopoulos secretly helped Jeffrey Epstein plan favorable TV appearances and media strategy.'),

    ('wexner', 'leslie-wexner-victorias-secret-epstein-power-attorney.html',
     'Victoria\'s Secret Billionaire Leslie Wexner Gave Epstein \'Full Power of Attorney\' Over $1 Billion Empire - Shocking DOJ Files Expose Total Control',
     'DOJ files reveal Leslie Wexner gave Jeffrey Epstein complete control over his Victoria\'s Secret fortune and personal life decisions worth over $1 billion.'),

    ('schwarzman', 'stephen-schwarzman-blackstone-epstein-connections.html',
     'Blackstone CEO Stephen Schwarzman\'s Secret Epstein Investment Calls: \'The Opportunities Are Extraordinary\'',
     'DOJ files reveal private equity titan Stephen Schwarzman discussed lucrative investments with Jeffrey Epstein in newly released phone records'),

    ('dershowitz', 'alan-dershowitz-epstein-legal-advice.html',
     'Harvard Law Professor Alan Dershowitz\'s Secret $300K Epstein Retainer: \'I Need You to Handle This Quietly\'',
     'DOJ files reveal Harvard\'s Alan Dershowitz received $300,000 from Epstein for \'special legal consultation\' in confidential arrangement.'),

    ('slim', 'carlos-slim-epstein-telecom-empire.html',
     'Mexican Billionaire Carlos Slim\'s Secret Epstein Telecom Deals: \'The Infrastructure Project Needs Your Touch\'',
     'DOJ files reveal Mexican telecom mogul Carlos Slim\'s hidden business relationship with Jeffrey Epstein involving major infrastructure deals.'),

    ('brin', 'sergey-brin-epstein-google-meetings.html',
     'Google Co-Founder Sergey Brin\'s Secret Epstein Meetings: \'We Need to Discuss the Algorithm Changes\'',
     'Shocking DOJ files reveal Google co-founder Sergey Brin held multiple private meetings with Jeffrey Epstein to discuss AI and search algorithm modifications.'),
]

for tag, href, title, lede in articles_to_fix:
    # Find the old pattern with lede outside article-title-section
    old_pattern = f'''<h2><a href="{href}">{title}</a></h2>
                    </div>
                </div>
                <p class="lede">{lede}</p>
                <a href="{href}" class="read-more">Read full article</a>
            </article>'''

    new_pattern = f'''<h2><a href="{href}">{title}</a></h2>
                        <p class="lede">{lede}</p>
                        <a href="{href}" class="read-more">Read full article</a>
                    </div>
                </div>
            </article>'''

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        print(f"✓ Fixed: {tag}")
    else:
        print(f"✗ Pattern not found for: {tag}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n" + "=" * 50)
print("Lede position fix complete!")
