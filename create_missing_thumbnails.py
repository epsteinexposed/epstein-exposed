#!/usr/bin/env python3
"""Create missing thumbnails for the 10 new articles."""

from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def create_authentic_email(output_path, to_email, from_email, sent_date, subject, body_lines, highlight_text=None, doc_number="DOJ-EPSTEIN-004521"):
    """Create authentic-looking leaked email with yellow highlight and navy DOJ bar"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    label_font = get_font(13, bold=True)
    value_font = get_font(13)
    body_font = get_font(13)
    sig_font = get_font(12)
    caption_font = get_font(10)

    y = 20
    left = 25
    label_width = 70

    # To field
    draw.text((left, y), "To:", fill='#000', font=label_font)
    draw.text((left + label_width, y), to_email, fill='#000', font=value_font)
    y += 24

    # From field
    draw.text((left, y), "From:", fill='#000', font=label_font)
    draw.text((left + label_width, y), from_email, fill='#000', font=value_font)
    y += 24

    # Sent field
    draw.text((left, y), "Sent:", fill='#000', font=label_font)
    draw.text((left + label_width, y), sent_date, fill='#000', font=value_font)
    y += 24

    # Subject field
    draw.text((left, y), "Subject:", fill='#000', font=label_font)
    draw.text((left + label_width + 15, y), subject, fill='#000', font=value_font)
    y += 38

    # Body text with yellow highlight
    for line in body_lines:
        if line == "":
            y += 14
            continue

        if highlight_text and highlight_text.lower() in line.lower():
            idx = line.lower().find(highlight_text.lower())
            before = line[:idx]
            word = line[idx:idx+len(highlight_text)]
            after = line[idx+len(highlight_text):]

            x = left
            if before:
                draw.text((x, y), before, fill='#000', font=body_font)
                x += draw.textlength(before, font=body_font)

            # Yellow highlight background
            word_w = draw.textlength(word, font=body_font)
            draw.rectangle([x - 2, y - 2, x + word_w + 2, y + 18], fill='#ffff00')
            draw.text((x, y), word, fill='#000', font=body_font)

            x += word_w
            if after:
                draw.text((x, y), after, fill='#000', font=body_font)
        else:
            draw.text((left, y), line, fill='#000', font=body_font)

        y += 22

    # BlackBerry signature
    y += 12
    draw.text((left, y), "Sent from my BlackBerry® wireless device", fill='#000', font=sig_font)

    # Dark navy bar at bottom with DOJ document number
    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created: {output_path}")

# Define thumbnails for each article
thumbnails = [
    {
        "filename": "images/alan-dershowitz-legal.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Alan Dershowitz[adersh@law.harvard.edu]",
        "sent_date": "Mon 3/12/2007 4:15:22 PM",
        "subject": "Re: Retainer Agreement",
        "body_lines": [
            "Jeffrey,",
            "",
            "Confirmed. I'll handle this quietly",
            "as discussed. The $300K covers all",
            "special consultation matters.",
        ],
        "highlight_text": "handle this quietly",
        "doc_number": "DOJ-EPSTEIN-004521"
    },
    {
        "filename": "images/carlos-slim-telecom.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Carlos Slim[cslim@telmex.com.mx]",
        "sent_date": "Thu 6/14/2012 2:30:45 PM",
        "subject": "Re: Telecom Investment",
        "body_lines": [
            "Jeffrey,",
            "",
            "The Latin America expansion is",
            "proceeding as planned. Your stake",
            "in the consortium is secured.",
        ],
        "highlight_text": "Your stake",
        "doc_number": "DOJ-EPSTEIN-008934"
    },
    {
        "filename": "images/george-stephanopoulos-abc.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "George Stephanopoulos[gsteph@abc.com]",
        "sent_date": "Tue 9/22/2015 11:20:33 AM",
        "subject": "Re: Interview Request",
        "body_lines": [
            "Jeffrey,",
            "",
            "I can make the dinner work.",
            "Let's keep this off the books",
            "for now - too much scrutiny.",
        ],
        "highlight_text": "off the books",
        "doc_number": "DOJ-EPSTEIN-012847"
    },
    {
        "filename": "images/leslie-wexner-victoria.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Leslie Wexner[lwexner@limitedbrands.com]",
        "sent_date": "Wed 4/18/2001 3:45:18 PM",
        "subject": "Re: Power of Attorney",
        "body_lines": [
            "Jeffrey,",
            "",
            "The POA documents are signed.",
            "You have full authority over",
            "the accounts as discussed.",
        ],
        "highlight_text": "full authority",
        "doc_number": "DOJ-EPSTEIN-001284"
    },
    {
        "filename": "images/naomi-campbell-charity.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Naomi Campbell[naomi@ncampbell.com]",
        "sent_date": "Fri 11/8/2008 6:12:44 PM",
        "subject": "Re: Charity Event Models",
        "body_lines": [
            "Jeffrey,",
            "",
            "I can send some of my girls",
            "for your foundation event.",
            "Let me know the dates.",
        ],
        "highlight_text": "my girls",
        "doc_number": "DOJ-EPSTEIN-007823"
    },
    {
        "filename": "images/oprah-winfrey-media.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Oprah Winfrey[oprah@harpo.com]",
        "sent_date": "Mon 2/14/2011 10:30:22 AM",
        "subject": "Re: Media Partnership",
        "body_lines": [
            "Jeffrey,",
            "",
            "The meeting at your townhouse",
            "was productive. Let's continue",
            "this conversation privately.",
        ],
        "highlight_text": "privately",
        "doc_number": "DOJ-EPSTEIN-009156"
    },
    {
        "filename": "images/sergey-brin-google.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Sergey Brin[sergey@google.com]",
        "sent_date": "Thu 5/22/2014 8:45:33 PM",
        "subject": "Re: Tech Investment Meeting",
        "body_lines": [
            "Jeffrey,",
            "",
            "Looking forward to the dinner",
            "at your island retreat next",
            "month. Bringing the family.",
        ],
        "highlight_text": "island retreat",
        "doc_number": "DOJ-EPSTEIN-011423"
    },
    {
        "filename": "images/stephen-schwarzman-blackstone.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Stephen Schwarzman[sschwarzman@blackstone.com]",
        "sent_date": "Tue 8/9/2005 4:22:15 PM",
        "subject": "Re: Investment Strategy",
        "body_lines": [
            "Jeffrey,",
            "",
            "The Blackstone arrangement",
            "is confirmed. Wire the funds",
            "to the offshore account.",
        ],
        "highlight_text": "offshore account",
        "doc_number": "DOJ-EPSTEIN-003847"
    },
    {
        "filename": "images/tom-barrack-trump.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "Tom Barrack[tbarrack@colony.com]",
        "sent_date": "Fri 10/14/2016 2:18:44 PM",
        "subject": "Re: Fundraiser Arrangements",
        "body_lines": [
            "Jeffrey,",
            "",
            "The inauguration fundraising",
            "is coming together. Your",
            "contribution is appreciated.",
        ],
        "highlight_text": "contribution",
        "doc_number": "DOJ-EPSTEIN-014562"
    },
    {
        "filename": "images/william-barr-doj.png",
        "to_email": "Jeffrey Epstein[jeevacation@gmail.com]",
        "from_email": "William Barr[wbarr@kirkland.com]",
        "sent_date": "Wed 7/18/2018 11:45:22 AM",
        "subject": "Re: Legal Consultation",
        "body_lines": [
            "Jeffrey,",
            "",
            "I've reviewed the situation.",
            "Will recuse myself from any",
            "matters involving your case.",
        ],
        "highlight_text": "recuse myself",
        "doc_number": "DOJ-EPSTEIN-016734"
    },
]

def main():
    print("Creating 10 missing thumbnails...")
    print("=" * 50)

    for thumb in thumbnails:
        create_authentic_email(
            thumb["filename"],
            thumb["to_email"],
            thumb["from_email"],
            thumb["sent_date"],
            thumb["subject"],
            thumb["body_lines"],
            thumb["highlight_text"],
            thumb["doc_number"]
        )

    print("=" * 50)
    print(f"Created {len(thumbnails)} thumbnails")

if __name__ == "__main__":
    main()
