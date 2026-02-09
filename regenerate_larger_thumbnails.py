#!/usr/bin/env python3
"""Regenerate all thumbnails at larger size (600x360)."""

from PIL import Image, ImageDraw, ImageFont

# New larger size
WIDTH, HEIGHT = 500, 300

def get_font(size, bold=False):
    if bold:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    else:
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def get_mono(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
    except:
        return ImageFont.load_default()

# ===== EMAIL THUMBNAIL =====
def create_email_thumbnail(output_path, to_email, from_email, sent_date, subject, body_lines, highlight_text=None, doc_number="DOJ-EPSTEIN-004521"):
    img = Image.new('RGB', (WIDTH, HEIGHT), '#ffffff')
    draw = ImageDraw.Draw(img)

    label_font = get_font(15, bold=True)
    value_font = get_font(15)
    body_font = get_font(15)
    sig_font = get_font(14)
    caption_font = get_font(12)

    y = 25
    left = 30
    label_width = 85

    draw.text((left, y), "To:", fill='#000', font=label_font)
    draw.text((left + label_width, y), to_email, fill='#000', font=value_font)
    y += 28

    draw.text((left, y), "From:", fill='#000', font=label_font)
    draw.text((left + label_width, y), from_email, fill='#000', font=value_font)
    y += 28

    draw.text((left, y), "Sent:", fill='#000', font=label_font)
    draw.text((left + label_width, y), sent_date, fill='#000', font=value_font)
    y += 28

    draw.text((left, y), "Subject:", fill='#000', font=label_font)
    draw.text((left + label_width + 15, y), subject, fill='#000', font=value_font)
    y += 45

    for line in body_lines:
        if line == "":
            y += 16
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
            word_w = draw.textlength(word, font=body_font)
            draw.rectangle([x - 2, y - 2, x + word_w + 2, y + 20], fill='#ffff00')
            draw.text((x, y), word, fill='#000', font=body_font)
            x += word_w
            if after:
                draw.text((x, y), after, fill='#000', font=body_font)
        else:
            draw.text((left, y), line, fill='#000', font=body_font)
        y += 26

    y += 15
    draw.text((left, y), "Sent from my BlackBerry® wireless device", fill='#000', font=sig_font)

    bar_height = 32
    draw.rectangle([0, HEIGHT - bar_height, WIDTH, HEIGHT], fill='#1a2744')
    draw.text((18, HEIGHT - bar_height + 9), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created EMAIL: {output_path}")


# ===== WIRE TRANSFER THUMBNAIL =====
def create_wire_thumbnail(output_path, date, sender, sender_account, recipient, recipient_account, amount, memo, highlight_text=None, doc_number="DOJ-EPSTEIN-FIN-01284"):
    img = Image.new('RGB', (WIDTH, HEIGHT), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(13, bold=True)
    label_font = get_font(13)
    value_font = get_font(13)
    amount_font = get_font(17, bold=True)
    caption_font = get_font(12)

    y = 20
    left = 30
    label_w = 140

    draw.text((left, y), "WIRE TRANSFER CONFIRMATION", fill='#000', font=header_font)
    y += 30

    fields = [
        ("Date:", date),
        ("Originator:", sender),
        ("Account:", sender_account),
        ("Beneficiary:", recipient),
        ("Beneficiary Acct:", recipient_account),
    ]

    for label, value in fields:
        draw.text((left, y), label, fill='#000', font=label_font)
        draw.text((left + label_w, y), value, fill='#000', font=value_font)
        y += 24

    y += 8

    draw.text((left, y), "Amount:", fill='#000', font=label_font)
    amount_x = left + label_w
    amount_w = draw.textlength(amount, font=amount_font)
    draw.rectangle([amount_x - 3, y - 3, amount_x + amount_w + 5, y + 24], fill='#ffff00')
    draw.text((amount_x, y), amount, fill='#000', font=amount_font)
    y += 34

    draw.text((left, y), "Memo:", fill='#000', font=label_font)
    memo_text = f'"{memo}"'
    if highlight_text and highlight_text.lower() in memo.lower():
        memo_w = draw.textlength(memo_text, font=value_font)
        draw.rectangle([left + label_w - 2, y - 2, left + label_w + memo_w + 4, y + 18], fill='#ffff00')
    draw.text((left + label_w, y), memo_text, fill='#000', font=value_font)

    bar_height = 32
    draw.rectangle([0, HEIGHT - bar_height, WIDTH, HEIGHT], fill='#1a2744')
    draw.text((18, HEIGHT - bar_height + 9), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created WIRE: {output_path}")


# ===== CALENDAR THUMBNAIL =====
def create_calendar_thumbnail(output_path, month, day, year, day_of_week, appointments, highlight_text=None, doc_number="DOJ-EPSTEIN-CAL-00384"):
    img = Image.new('RGB', (WIDTH, HEIGHT), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(12, bold=True)
    month_font = get_font(14, bold=True)
    day_font = get_font(50, bold=True)
    weekday_font = get_font(12)
    time_font = get_font(13, bold=True)
    event_font = get_font(13)
    caption_font = get_font(12)

    draw.text((30, 15), "PERSONAL CALENDAR - CONFIDENTIAL", fill='#000', font=header_font)

    box_x, box_y = 30, 45
    box_w, box_h = 120, 115

    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 30], fill='#cc0000')
    draw.text((box_x + 30, box_y + 6), month.upper(), fill='#fff', font=month_font)

    draw.rectangle([box_x, box_y + 30, box_x + box_w, box_y + box_h], fill='#fff', outline='#ccc', width=1)

    day_text = str(day)
    day_w = draw.textlength(day_text, font=day_font)
    draw.text((box_x + (box_w - day_w) / 2, box_y + 42), day_text, fill='#000', font=day_font)

    weekday_w = draw.textlength(day_of_week, font=weekday_font)
    draw.text((box_x + (box_w - weekday_w) / 2, box_y + 95), day_of_week, fill='#666', font=weekday_font)

    year_text = str(year)
    year_w = draw.textlength(year_text, font=weekday_font)
    draw.text((box_x + (box_w - year_w) / 2, box_y + box_h + 8), year_text, fill='#666', font=weekday_font)

    appt_x = 175
    appt_y = 55

    draw.text((appt_x, appt_y), "APPOINTMENTS:", fill='#000', font=header_font)
    appt_y += 28

    for time, event in appointments:
        should_highlight = highlight_text and highlight_text.lower() in event.lower()
        draw.text((appt_x, appt_y), time, fill='#cc0000', font=time_font)
        event_x = appt_x + 85
        if should_highlight:
            event_w = draw.textlength(event, font=event_font)
            draw.rectangle([event_x - 2, appt_y - 2, event_x + event_w + 4, appt_y + 18], fill='#ffff00')
        draw.text((event_x, appt_y), event, fill='#000', font=event_font)
        appt_y += 26

    bar_height = 32
    draw.rectangle([0, HEIGHT - bar_height, WIDTH, HEIGHT], fill='#1a2744')
    draw.text((18, HEIGHT - bar_height + 9), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    img.save(output_path, quality=95)
    print(f"Created CALENDAR: {output_path}")


# ===== CREATE ALL THUMBNAILS =====
def main():
    print(f"Creating larger thumbnails ({WIDTH}x{HEIGHT})...")
    print("=" * 50)

    # EMAIL: Dershowitz - Legal retainer
    create_email_thumbnail(
        "images/alan-dershowitz-legal.png",
        to_email="Jeffrey Epstein[jeevacation@gmail.com]",
        from_email="Alan Dershowitz[adersh@law.harvard.edu]",
        sent_date="Mon 3/12/2007 4:15:22 PM",
        subject="Re: Retainer Agreement",
        body_lines=["Jeffrey,", "", "Confirmed. I'll handle this quietly", "as discussed. The $300K covers all", "special consultation matters."],
        highlight_text="handle this quietly",
        doc_number="DOJ-EPSTEIN-004521"
    )

    # WIRE: Carlos Slim - Telecom investment
    create_wire_thumbnail(
        "images/carlos-slim-telecom.png",
        date="June 14, 2012",
        sender="Telmex Holdings S.A.",
        sender_account="****7823",
        recipient="JE Investment Partners LLC",
        recipient_account="****4156",
        amount="$15,000,000.00",
        memo="Latin America infrastructure consortium",
        highlight_text="consortium",
        doc_number="DOJ-EPSTEIN-FIN-08934"
    )

    # EMAIL: Stephanopoulos - Interview coordination
    create_email_thumbnail(
        "images/george-stephanopoulos-abc.png",
        to_email="Jeffrey Epstein[jeevacation@gmail.com]",
        from_email="George Stephanopoulos[gsteph@abc.com]",
        sent_date="Tue 9/22/2015 11:20:33 AM",
        subject="Re: Interview Request",
        body_lines=["Jeffrey,", "", "I can make the dinner work.", "Let's keep this off the books", "for now - too much scrutiny."],
        highlight_text="off the books",
        doc_number="DOJ-EPSTEIN-012847"
    )

    # CALENDAR: Leslie Wexner - Meetings
    create_calendar_thumbnail(
        "images/leslie-wexner-victoria.png",
        month="APR",
        day=18,
        year=2001,
        day_of_week="Wednesday",
        appointments=[
            ("10:00 AM", "POA signing - Wexner"),
            ("2:00 PM", "Victoria's Secret review"),
            ("6:00 PM", "Dinner: Les & Abigail"),
        ],
        highlight_text="POA signing",
        doc_number="DOJ-EPSTEIN-CAL-01284"
    )

    # EMAIL: Naomi Campbell - Charity
    create_email_thumbnail(
        "images/naomi-campbell-charity.png",
        to_email="Jeffrey Epstein[jeevacation@gmail.com]",
        from_email="Naomi Campbell[naomi@ncampbell.com]",
        sent_date="Fri 11/8/2008 6:12:44 PM",
        subject="Re: Charity Event Models",
        body_lines=["Jeffrey,", "", "I can send some of my girls", "for your foundation event.", "Let me know the dates."],
        highlight_text="my girls",
        doc_number="DOJ-EPSTEIN-007823"
    )

    # CALENDAR: Oprah - Media meetings
    create_calendar_thumbnail(
        "images/oprah-winfrey-media.png",
        month="FEB",
        day=14,
        year=2011,
        day_of_week="Monday",
        appointments=[
            ("11:00 AM", "Oprah - media strategy"),
            ("3:00 PM", "Call re: victim narratives"),
            ("7:00 PM", "Private dinner - townhouse"),
        ],
        highlight_text="victim narratives",
        doc_number="DOJ-EPSTEIN-CAL-09156"
    )

    # CALENDAR: Sergey Brin - Tech meetings
    create_calendar_thumbnail(
        "images/sergey-brin-google.png",
        month="MAY",
        day=22,
        year=2014,
        day_of_week="Thursday",
        appointments=[
            ("2:00 PM", "Sergey Brin - island arrival"),
            ("5:00 PM", "AI/Algorithm discussion"),
            ("8:00 PM", "Dinner with Brin family"),
        ],
        highlight_text="island arrival",
        doc_number="DOJ-EPSTEIN-CAL-11423"
    )

    # WIRE: Stephen Schwarzman - Blackstone
    create_wire_thumbnail(
        "images/stephen-schwarzman-blackstone.png",
        date="August 9, 2005",
        sender="Blackstone Group LP",
        sender_account="****9234",
        recipient="Gratitude America Ltd",
        recipient_account="****7712",
        amount="$10,000,000.00",
        memo="Private equity co-investment - offshore",
        highlight_text="offshore",
        doc_number="DOJ-EPSTEIN-FIN-03847"
    )

    # WIRE: Tom Barrack - Fundraising
    create_wire_thumbnail(
        "images/tom-barrack-trump.png",
        date="October 14, 2016",
        sender="Colony Capital LLC",
        sender_account="****5521",
        recipient="JE Foundation",
        recipient_account="****8834",
        amount="$2,500,000.00",
        memo="Inauguration fund contribution",
        highlight_text="Inauguration",
        doc_number="DOJ-EPSTEIN-FIN-14562"
    )

    # EMAIL: William Barr - DOJ
    create_email_thumbnail(
        "images/william-barr-doj.png",
        to_email="Jeffrey Epstein[jeevacation@gmail.com]",
        from_email="William Barr[wbarr@kirkland.com]",
        sent_date="Wed 7/18/2018 11:45:22 AM",
        subject="Re: Legal Consultation",
        body_lines=["Jeffrey,", "", "I've reviewed the situation.", "Will recuse myself from any", "matters involving your case."],
        highlight_text="recuse myself",
        doc_number="DOJ-EPSTEIN-016734"
    )

    print("=" * 50)
    print(f"Created 10 larger thumbnails at {WIDTH}x{HEIGHT}")

if __name__ == "__main__":
    main()
