#!/usr/bin/env python3
"""
Epstein Files Daily - Authentic Thumbnail Generator
All styles have: yellow highlights, dark navy DOJ bar at bottom

Usage: Import this file and call the appropriate function for your article type.
"""

from PIL import Image, ImageDraw, ImageFont
import os

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


# ============================================
# 📧 EMAIL THUMBNAIL (default)
# ============================================
def create_email_thumbnail(output_path, to_email, from_email, sent_date, subject,
                           body_lines, highlight_text=None, doc_number="DOJ-EPSTEIN-004521"):
    """Create authentic leaked email thumbnail"""

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

    draw.text((left, y), "To:", fill='#000', font=label_font)
    draw.text((left + label_width, y), to_email, fill='#000', font=value_font)
    y += 24

    draw.text((left, y), "From:", fill='#000', font=label_font)
    draw.text((left + label_width, y), from_email, fill='#000', font=value_font)
    y += 24

    draw.text((left, y), "Sent:", fill='#000', font=label_font)
    draw.text((left + label_width, y), sent_date, fill='#000', font=value_font)
    y += 24

    draw.text((left, y), "Subject:", fill='#000', font=label_font)
    draw.text((left + label_width + 15, y), subject, fill='#000', font=value_font)
    y += 38

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

            word_w = draw.textlength(word, font=body_font)
            draw.rectangle([x - 2, y - 2, x + word_w + 2, y + 18], fill='#ffff00')
            draw.text((x, y), word, fill='#000', font=body_font)
            x += word_w

            if after:
                draw.text((x, y), after, fill='#000', font=body_font)
        else:
            draw.text((left, y), line, fill='#000', font=body_font)
        y += 22

    y += 12
    draw.text((left, y), "Sent from my BlackBerry® wireless device", fill='#000', font=sig_font)

    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")


# ============================================
# ✈️ FLIGHT LOG THUMBNAIL
# ============================================
def create_flight_thumbnail(output_path, flight_date, origin, destination, tail_number,
                            passengers, highlight_passenger, doc_number="DOJ-EPSTEIN-FL-00847"):
    """Create authentic flight manifest thumbnail"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    label_font = get_font(11)
    mono_font = get_mono(11)
    caption_font = get_font(10)

    y = 15
    left = 25

    draw.text((left, y), "FLIGHT MANIFEST - CONFIDENTIAL", fill='#000', font=header_font)
    y += 25

    draw.text((left, y), "Date:", fill='#000', font=label_font)
    draw.text((left + 80, y), flight_date, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Origin:", fill='#000', font=label_font)
    draw.text((left + 80, y), origin, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Destination:", fill='#000', font=label_font)
    draw.text((left + 80, y), destination, fill='#000', font=mono_font)
    y += 20

    draw.text((left, y), "Aircraft:", fill='#000', font=label_font)
    draw.text((left + 80, y), f"{tail_number} (Gulfstream IV)", fill='#000', font=mono_font)
    y += 28

    draw.text((left, y), "PASSENGERS:", fill='#000', font=header_font)
    y += 22

    for i, passenger in enumerate(passengers):
        text = f"{i+1}. {passenger}"
        if highlight_passenger and highlight_passenger.lower() in passenger.lower():
            text_w = draw.textlength(text, font=mono_font)
            draw.rectangle([left - 2, y - 2, left + text_w + 4, y + 16], fill='#ffff00')
        draw.text((left, y), text, fill='#000', font=mono_font)
        y += 18

    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")


# ============================================
# 💰 WIRE TRANSFER THUMBNAIL
# ============================================
def create_wire_thumbnail(output_path, date, sender, sender_account, recipient,
                          recipient_account, amount, memo, highlight_text=None,
                          doc_number="DOJ-EPSTEIN-FIN-01284"):
    """Create authentic wire transfer thumbnail"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    label_font = get_font(11)
    value_font = get_font(11)
    amount_font = get_font(14, bold=True)
    caption_font = get_font(10)

    y = 15
    left = 25
    label_w = 120

    draw.text((left, y), "WIRE TRANSFER CONFIRMATION", fill='#000', font=header_font)
    y += 25

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
        y += 20

    y += 5
    draw.text((left, y), "Amount:", fill='#000', font=label_font)
    amount_x = left + label_w
    amount_w = draw.textlength(amount, font=amount_font)
    draw.rectangle([amount_x - 3, y - 3, amount_x + amount_w + 5, y + 20], fill='#ffff00')
    draw.text((amount_x, y), amount, fill='#000', font=amount_font)
    y += 28

    draw.text((left, y), "Memo:", fill='#000', font=label_font)
    memo_text = f'"{memo}"'
    if highlight_text and highlight_text.lower() in memo.lower():
        memo_w = draw.textlength(memo_text, font=value_font)
        draw.rectangle([left + label_w - 2, y - 2, left + label_w + memo_w + 4, y + 16], fill='#ffff00')
    draw.text((left + label_w, y), memo_text, fill='#000', font=value_font)

    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")


# ============================================
# 📅 CALENDAR THUMBNAIL
# ============================================
def create_calendar_thumbnail(output_path, month, day, year, day_of_week, appointments,
                              highlight_text=None, doc_number="DOJ-EPSTEIN-CAL-00384"):
    """Create authentic calendar thumbnail with visual day box"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#ffffff')
    draw = ImageDraw.Draw(img)

    header_font = get_font(10, bold=True)
    month_font = get_font(12, bold=True)
    day_font = get_font(42, bold=True)
    weekday_font = get_font(10)
    time_font = get_font(11, bold=True)
    event_font = get_font(11)
    caption_font = get_font(10)

    draw.text((25, 12), "PERSONAL CALENDAR - CONFIDENTIAL", fill='#000', font=header_font)

    box_x, box_y = 25, 38
    box_w, box_h = 100, 95

    draw.rectangle([box_x, box_y, box_x + box_w, box_y + 25], fill='#cc0000')
    draw.text((box_x + 25, box_y + 5), month.upper(), fill='#fff', font=month_font)

    draw.rectangle([box_x, box_y + 25, box_x + box_w, box_y + box_h], fill='#fff', outline='#ccc', width=1)

    day_text = str(day)
    day_w = draw.textlength(day_text, font=day_font)
    draw.text((box_x + (box_w - day_w) / 2, box_y + 35), day_text, fill='#000', font=day_font)

    weekday_w = draw.textlength(day_of_week, font=weekday_font)
    draw.text((box_x + (box_w - weekday_w) / 2, box_y + 78), day_of_week, fill='#666', font=weekday_font)

    year_text = str(year)
    year_w = draw.textlength(year_text, font=weekday_font)
    draw.text((box_x + (box_w - year_w) / 2, box_y + box_h + 5), year_text, fill='#666', font=weekday_font)

    appt_x = 145
    appt_y = 45

    draw.text((appt_x, appt_y), "APPOINTMENTS:", fill='#000', font=header_font)
    appt_y += 22

    for time, event in appointments:
        should_highlight = highlight_text and highlight_text.lower() in event.lower()
        draw.text((appt_x, appt_y), time, fill='#cc0000', font=time_font)
        event_x = appt_x + 70
        if should_highlight:
            event_w = draw.textlength(event, font=event_font)
            draw.rectangle([event_x - 2, appt_y - 2, event_x + event_w + 4, appt_y + 16], fill='#ffff00')
        draw.text((event_x, appt_y), event, fill='#000', font=event_font)
        appt_y += 22

    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")


# ============================================
# 💬 TEXT MESSAGE THUMBNAIL
# ============================================
def create_text_thumbnail(output_path, contact_name, phone_number, messages,
                          highlight_text=None, doc_number="DOJ-EPSTEIN-DIG-02847"):
    """Create authentic text message forensic extraction thumbnail"""

    width, height = 500, 300
    img = Image.new('RGB', (width, height), '#f5f5f5')
    draw = ImageDraw.Draw(img)

    header_font = get_font(11, bold=True)
    contact_font = get_font(12, bold=True)
    msg_font = get_font(11)
    time_font = get_font(9)
    caption_font = get_font(10)

    y = 15
    left = 25

    draw.text((left, y), "TEXT MESSAGE EXTRACTION - FORENSIC COPY", fill='#000', font=header_font)
    y += 22

    draw.text((left, y), f"Contact: {contact_name}", fill='#000', font=contact_font)
    y += 18
    draw.text((left, y), f"Phone: {phone_number}", fill='#666', font=msg_font)
    y += 25

    for sender, text, timestamp in messages:
        is_epstein = sender.lower() == "epstein"
        bubble_x = left if not is_epstein else left + 150
        bubble_color = '#e5e5ea' if not is_epstein else '#007aff'
        text_color = '#000' if not is_epstein else '#fff'

        should_highlight = highlight_text and highlight_text.lower() in text.lower()
        text_w = min(draw.textlength(text, font=msg_font), 280)
        bubble_w = text_w + 20

        if should_highlight:
            draw.rectangle([bubble_x - 3, y - 3, bubble_x + bubble_w + 5, y + 40], outline='#ffff00', width=3)

        draw.rounded_rectangle([bubble_x, y, bubble_x + bubble_w, y + 35], radius=10, fill=bubble_color)
        draw.text((bubble_x + 10, y + 8), text[:40], fill=text_color, font=msg_font)
        draw.text((bubble_x + 10, y + 38), timestamp, fill='#888', font=time_font)
        y += 55

    bar_height = 28
    draw.rectangle([0, height - bar_height, width, height], fill='#1a2744')
    draw.text((15, height - bar_height + 8), f"U.S. Department of Justice  •  {doc_number}", fill='#ffffff', font=caption_font)

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "images", exist_ok=True)
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")


if __name__ == "__main__":
    print("Epstein Files Daily - Thumbnail Generator")
    print("=" * 50)
    print()
    print("Available functions:")
    print("  create_email_thumbnail()    - For correspondence (default)")
    print("  create_flight_thumbnail()   - For travel/flights")
    print("  create_wire_thumbnail()     - For financial records")
    print("  create_calendar_thumbnail() - For meetings/dinners")
    print("  create_text_thumbnail()     - For text messages")
