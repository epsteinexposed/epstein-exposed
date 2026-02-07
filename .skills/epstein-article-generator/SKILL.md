---
name: epstein-article-generator
description: |
  Generate new articles for Epstein Files Daily website based on DOJ document releases.
  TRIGGERS: "write new article", "generate article", "publish article", "daily article", "epstein article"
  Finds interesting DOJ documents, writes SEO-optimized investigative articles, creates thumbnails, updates the site, and pushes to GitHub.
---

# Epstein Article Generator

Generate investigative journalism articles for epsteinfilesdaily.com based on DOJ file releases.

## ⚠️ CRITICAL CHECKLIST - VERIFY BEFORE PUBLISHING

Before pushing ANY article, confirm ALL of these are complete:

- [ ] **Article created FROM TEMPLATE** - MUST copy `references/article-template.html` as base
- [ ] **Article has theme-toggle** - Verify with: `grep -c "theme-toggle" article.html` (should return 6)
- [ ] **Thumbnail image created** in `images/` folder
- [ ] **index.html updated** with article card INCLUDING thumbnail `<img>` tag
- [ ] **feed.xml updated** with new `<item>`
- [ ] **covered-topics.md updated** with new topic
- [ ] **Tags use FULL NAMES** (e.g., "woody allen" not "allen")

**DO NOT SKIP THE THUMBNAIL** - Articles without thumbnails look broken on the site.

## 🚨 MANDATORY: USE THE TEMPLATE FILE

**NEVER write article HTML from scratch.** ALWAYS:
1. Read `references/article-template.html` first
2. Copy it as the base for your new article
3. Only replace the placeholder content ({{HEADLINE}}, {{SLUG}}, etc.)

The template includes critical features that MUST be present:
- Dark theme CSS with CSS variables
- Light/dark mode toggle in header
- Search bar in header
- Sticky header with red accent
- Theme persistence JavaScript
- Correct "Epstein Files Daily" branding
- EF favicon (not EE)

**If your article is missing any of these, it will look broken on the site.**

---

## Workflow

### Step 1: Check Covered Topics

Read `references/covered-topics.md` to see what's already published. Do NOT repeat stories.

### Step 2: Find New Source Material

Search DOJ Epstein files (https://www.justice.gov/epstein) for interesting stories:
- **Documents/Emails**: PDFs with revealing correspondence
- **Images**: Photos from the releases
- **Videos**: Depositions or footage
- **Flight logs**: Lolita Express passenger records
- **Financial records**: Wire transfers, payments

**Prioritize lesser-known names** over repeated coverage of big names. Look for:
- Business executives, foreign dignitaries, entertainment figures
- Academics/scientists, financial industry connections
- Real estate deals, foundation/charity connections

### Step 3: Verify Sources

- **ONLY use DOJ sources** - NO external news sources (PBS, CBS, CNN, etc.)
- Only use real DOJ document IDs (format: EFTAxxxxxxxx.pdf)
- Verify URLs exist at justice.gov
- Quote directly from documents
- All source-box links must point to justice.gov/epstein domains

### Step 4: Write Article (MUST USE TEMPLATE)

**⚠️ CRITICAL: You MUST use the template file. DO NOT write HTML from scratch.**

**Step 4a: Read the template first**
```bash
cat references/article-template.html
```

**Step 4b: Copy template and replace placeholders**

The template uses these placeholders - replace ALL of them:
- `{{HEADLINE}}` - Article headline
- `{{META_DESCRIPTION}}` - SEO description (150-160 chars)
- `{{SLUG}}` - URL slug (e.g., `martha-stewart-epstein-parties`)
- `{{THUMBNAIL_FILENAME}}` - Thumbnail filename without extension
- `{{PERSON_TAG}}` - Person's full name for tag
- `{{DATE}}` - Publication date
- `{{ARTICLE_CONTENT}}` - The actual article body

**Step 4c: Verify article has required features**
```bash
# Must return 6 (theme toggle elements)
grep -c "theme-toggle" your-article.html

# Must return matches (dark theme CSS)
grep "var(--bg)" your-article.html | head -1
```

**Article Elements:**
- **Headline**: Attention-grabbing, uses quotes from docs when possible
- **Lede**: 1-2 sentence hook summarizing the revelation
- **Body**: Opening context, document evidence box, analysis, response box, source box, share buttons

**SEO**: Title <60 chars, meta description 150-160 chars, full name in title/first paragraph

**Style**: Tabloid tone but factual, short paragraphs, pull quotes for damning evidence

### Step 5: Create Thumbnail Image (MANDATORY)

**⚠️ THIS STEP IS REQUIRED - DO NOT SKIP**

Choose the appropriate thumbnail style based on the source material:

| Style | Use When |
|-------|----------|
| 📧 **Email** | Email correspondence, memos, personal communications |
| ✈️ **Flight Log** | Lolita Express records, travel logs, passenger lists |
| 💰 **Wire Transfer** | Financial records, payments, donations, money trails |
| 📅 **Calendar** | Meetings, appointments, dinner parties, scheduled events |
| 💬 **Text Message** | Text conversations, chat logs, informal communications |

**Thumbnail filename format**: `firstname-lastname-topic.png` (lowercase, hyphens)

---

#### 📧 STYLE 1: EMAIL (Default)
Use for: Email correspondence, memos, personal communications

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_email_thumbnail(filename, doc_id, to_field, from_field, date_field, highlight_text):
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (250, 250, 247))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 32)
        font_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except:
        font_header = font_label = font_value = font_highlight = ImageFont.load_default()

    # Dark slate header
    draw.rectangle([(0, 0), (WIDTH, 50)], fill=(51, 65, 85))
    draw.text((20, 12), f"📁 DOJ EPSTEIN FILES — {doc_id}", font=font_header, fill=(255, 255, 255))

    # Red accent bar
    draw.rectangle([(0, 50), (18, HEIGHT)], fill=(220, 38, 38))

    # Email fields
    y = 95
    for label, value in [("To:", to_field), ("From:", from_field), ("Date:", date_field)]:
        draw.text((55, y), label, font=font_label, fill=(120, 120, 120))
        draw.text((160, y), value, font=font_value, fill=(40, 40, 40))
        y += 50
    y += 20

    # Highlighted quote with word wrap
    max_width = WIDTH - 120
    words = highlight_text.split()
    lines, current_line = [], []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font_highlight)
        if bbox[2] - bbox[0] > max_width and current_line:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line: lines.append(' '.join(current_line))

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font_highlight)
        draw.rectangle([(50, y - 5), (60 + bbox[2] - bbox[0], y + bbox[3] - bbox[1] + 10)], fill=(255, 247, 140))
        draw.text((55, y), line, font=font_highlight, fill=(40, 40, 40))
        y += bbox[3] - bbox[1] + 22

    os.makedirs("images", exist_ok=True)
    img.save(f"images/{filename}", 'PNG')
    print(f"Created: images/{filename}")

# Usage:
create_email_thumbnail("person-topic.png", "EFTA00123456.pdf", "Jeffrey Epstein", "Person Name", "March 15, 2005", "The damning quote here")
```

---

#### ✈️ STYLE 2: FLIGHT LOG
Use for: Lolita Express records, travel logs, passenger lists

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_flight_thumbnail(filename, doc_id, flight_date, origin, destination, passengers, highlight_passenger):
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (245, 245, 240))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 22)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_stamp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
    except:
        font_header = font_mono = font_medium = font_stamp = ImageFont.load_default()

    # Navy header
    draw.rectangle([(0, 0), (WIDTH, 55)], fill=(25, 55, 95))
    draw.text((20, 14), f"✈️ LOLITA EXPRESS — FLIGHT MANIFEST", font=font_header, fill=(255, 255, 255))
    draw.text((WIDTH - 250, 18), doc_id, font=font_mono, fill=(180, 200, 220))

    # Red accent
    draw.rectangle([(0, 55), (12, HEIGHT)], fill=(220, 38, 38))

    # Table header
    y = 80
    draw.rectangle([(30, y), (WIDTH - 30, y + 45)], fill=(230, 235, 245))
    cols = [50, 200, 400, 600, 900]
    for col, header in zip(cols, ["DATE", "FROM", "TO", "PASSENGERS", "TAIL#"]):
        draw.text((col, y + 10), header, font=font_mono, fill=(60, 60, 80))

    # Flight row (highlighted)
    y += 55
    draw.rectangle([(30, y), (WIDTH - 30, y + 50)], fill=(255, 247, 140))
    for col, val in zip(cols, [flight_date, origin, destination, highlight_passenger, "N908JE"]):
        draw.text((col, y + 12), val, font=font_mono, fill=(40, 40, 40))

    # Additional passengers
    y += 70
    draw.text((50, y), "Full passenger manifest:", font=font_medium, fill=(80, 80, 80))
    y += 40
    draw.text((50, y), passengers, font=font_medium, fill=(40, 40, 40))

    # CLASSIFIED stamp
    draw.text((800, 400), "CLASSIFIED", font=font_stamp, fill=(220, 38, 38))

    # Footer
    draw.rectangle([(0, HEIGHT - 50), (WIDTH, HEIGHT)], fill=(240, 240, 235))
    draw.text((30, HEIGHT - 38), f"Source: DOJ Epstein Document Release — {doc_id}", font=font_mono, fill=(120, 120, 120))

    os.makedirs("images", exist_ok=True)
    img.save(f"images/{filename}", 'PNG')
    print(f"Created: images/{filename}")

# Usage:
create_flight_thumbnail("person-flight.png", "EFTA00923847.pdf", "03/15/2002", "TETERBORO", "ST. THOMAS", "J. Epstein, G. Maxwell, Person Name, +2 others", "PERSON NAME")
```

---

#### 💰 STYLE 3: WIRE TRANSFER
Use for: Financial records, payments, donations, money trails

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_wire_thumbnail(filename, doc_id, date, sender, recipient, amount, memo):
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (250, 252, 255))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_amount = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 42)
        font_stamp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except:
        font_header = font_mono = font_medium = font_amount = font_stamp = ImageFont.load_default()

    # Green header (bank style)
    draw.rectangle([(0, 0), (WIDTH, 55)], fill=(0, 80, 60))
    draw.text((20, 14), "💰 WIRE TRANSFER CONFIRMATION", font=font_header, fill=(255, 255, 255))

    # Gold accent
    draw.rectangle([(0, 55), (12, HEIGHT)], fill=(180, 140, 20))

    # Transfer details
    y = 90
    for label, value in [("Date:", date), ("Originator:", sender), ("Beneficiary:", recipient)]:
        draw.text((50, y), label, font=font_mono, fill=(100, 100, 100))
        draw.text((280, y), value, font=font_medium, fill=(30, 30, 30))
        y += 50

    # Highlighted amount
    y += 20
    draw.rectangle([(40, y - 10), (550, y + 70)], fill=(255, 247, 140))
    draw.text((50, y), "AMOUNT:", font=font_mono, fill=(100, 100, 100))
    draw.text((280, y + 5), amount, font=font_amount, fill=(180, 50, 50))

    # Memo
    y += 100
    draw.rectangle([(40, y), (WIDTH - 40, y + 70)], fill=(245, 245, 250), outline=(200, 200, 210))
    draw.text((60, y + 20), f'MEMO: "{memo}"', font=font_medium, fill=(60, 60, 60))

    # SUBPOENAED stamp
    draw.text((800, 180), "SUBPOENAED", font=font_stamp, fill=(220, 38, 38))

    # Footer
    draw.rectangle([(0, HEIGHT - 50), (WIDTH, HEIGHT)], fill=(240, 245, 250))
    draw.text((30, HEIGHT - 38), f"Source: DOJ Epstein Financial Records — {doc_id}", font=font_mono, fill=(120, 120, 120))

    os.makedirs("images", exist_ok=True)
    img.save(f"images/{filename}", 'PNG')
    print(f"Created: images/{filename}")

# Usage:
create_wire_thumbnail("person-payment.png", "EFTA01284756.pdf", "September 14, 2008", "GRATITUDE AMERICA LTD", "PERSON NAME", "$2,500,000.00", "Consulting services")
```

---

#### 📅 STYLE 4: CALENDAR
Use for: Meetings, appointments, dinner parties, scheduled events

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_calendar_thumbnail(filename, doc_id, month, day, weekday, appointments, notes):
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (250, 250, 247))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_day = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 26)
        font_time = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 20)
    except:
        font_header = font_day = font_medium = font_time = font_mono = ImageFont.load_default()

    # Purple header
    draw.rectangle([(0, 0), (WIDTH, 55)], fill=(90, 50, 120))
    draw.text((20, 14), "📅 EPSTEIN PERSONAL CALENDAR", font=font_header, fill=(255, 255, 255))

    # Purple accent
    draw.rectangle([(0, 55), (12, HEIGHT)], fill=(140, 80, 180))

    # Calendar day box
    draw.rectangle([(40, 80), (180, 220)], fill=(245, 240, 250), outline=(140, 80, 180), width=3)
    draw.text((70, 90), month, font=font_medium, fill=(140, 80, 180))
    draw.text((65, 130), day, font=font_day, fill=(60, 30, 80))
    draw.text((60, 195), weekday, font=font_mono, fill=(100, 100, 100))

    # Appointments (list of tuples: time, description, highlight)
    y = 90
    for time, desc, highlight in appointments:
        if highlight:
            draw.rectangle([(210, y - 5), (WIDTH - 50, y + 40)], fill=(255, 247, 140))
        draw.text((220, y), time, font=font_time, fill=(140, 80, 180))
        draw.text((370, y + 2), desc, font=font_medium, fill=(40, 40, 40))
        y += 55

    # Notes section
    y += 30
    draw.rectangle([(40, y), (WIDTH - 40, y + 80)], fill=(255, 255, 245), outline=(200, 200, 190))
    draw.text((60, y + 15), "NOTES:", font=font_mono, fill=(150, 150, 150))
    draw.text((60, y + 45), f'"{notes}"', font=font_medium, fill=(60, 60, 60))

    # Footer
    draw.rectangle([(0, HEIGHT - 50), (WIDTH, HEIGHT)], fill=(245, 240, 250))
    draw.text((30, HEIGHT - 38), f"Source: DOJ Epstein Document Release — {doc_id}", font=font_mono, fill=(120, 120, 120))

    os.makedirs("images", exist_ok=True)
    img.save(f"images/{filename}", 'PNG')
    print(f"Created: images/{filename}")

# Usage (appointments is list of tuples: time, description, highlight_bool):
create_calendar_thumbnail("person-dinner.png", "EFTA00384756.pdf", "MAR", "14", "Monday",
    [("2:00 PM", "Person Name - tea at 71st St", True), ("8:00 PM", "Dinner: Person, Guest1, Guest2", False)],
    "Call Ghislaine re: arrangements")
```

---

#### 💬 STYLE 5: TEXT MESSAGE
Use for: Text conversations, chat logs, informal communications

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_text_thumbnail(filename, doc_id, contact_name, messages):
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (30, 30, 35))
    draw = ImageDraw.Draw(img)

    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_contact = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_msg = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_time = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 16)
    except:
        font_header = font_contact = font_msg = font_time = font_mono = ImageFont.load_default()

    # Status bar
    draw.rectangle([(0, 0), (WIDTH, 55)], fill=(20, 20, 25))
    draw.text((20, 14), "💬 TEXT MESSAGES — RECOVERED FROM DEVICE", font=font_header, fill=(255, 255, 255))

    # Contact header
    draw.rectangle([(0, 55), (WIDTH, 110)], fill=(45, 45, 50))
    draw.ellipse([(30, 65), (90, 125)], fill=(80, 80, 90))
    initials = ''.join([n[0] for n in contact_name.split()[:2]])
    draw.text((45, 78), initials, font=font_contact, fill=(200, 200, 200))
    draw.text((110, 72), contact_name, font=font_contact, fill=(255, 255, 255))

    # Messages (list of tuples: text, timestamp, is_outgoing, is_highlighted)
    y = 130
    for text, timestamp, is_outgoing, is_highlighted in messages:
        x = 450 if is_outgoing else 40
        max_w = WIDTH - 490 if is_outgoing else 700
        bg_color = (0, 120, 255) if is_outgoing else (60, 60, 65)

        # Message bubble
        draw.rounded_rectangle([(x, y), (x + max_w, y + 70)], radius=15, fill=bg_color)
        if is_highlighted:
            draw.rectangle([(x - 5, y - 5), (x + max_w + 5, y + 75)], outline=(255, 220, 50), width=3)
        draw.text((x + 15, y + 12), text[:60], font=font_msg, fill=(255, 255, 255))
        draw.text((x + 15, y + 45), timestamp, font=font_time, fill=(180, 180, 180))
        y += 90

    # Footer
    draw.rectangle([(0, HEIGHT - 50), (WIDTH, HEIGHT)], fill=(20, 20, 25))
    draw.text((30, HEIGHT - 38), f"Source: DOJ Digital Forensics — {doc_id}", font=font_mono, fill=(120, 120, 120))

    os.makedirs("images", exist_ok=True)
    img.save(f"images/{filename}", 'PNG')
    print(f"Created: images/{filename}")

# Usage (messages is list of tuples: text, timestamp, is_outgoing, is_highlighted):
create_text_thumbnail("person-texts.png", "EFTA02847561.pdf", "Person Name", [
    ("Got the girls for the trip", "Mar 12, 3:42 PM", False, False),
    ("Perfect. Same arrangement as before", "Mar 12, 3:45 PM", True, True),
    ("Confirmed for Saturday", "Mar 12, 4:12 PM", False, True)
])
```

---

**After creating thumbnail, verify it exists:**
```bash
ls -la images/firstname-lastname-topic.png
```

### Step 6: Save Article

Save HTML to workspace: `firstname-lastname-topic.html` (lowercase, hyphens)

### Step 7: Update Site

#### 7a. Add article card to `index.html`

**IMPORTANT**: The article card MUST include the thumbnail image. Use this exact format:

```html
<!-- AUTO-GENERATED ARTICLE: FIRSTNAME LASTNAME -->
<article class="article-preview featured" data-tags="firstname lastname">
    <div class="article-top">
        <a href="firstname-lastname-topic.html" class="article-thumb">
            <img src="images/firstname-lastname-topic.png?v=1" alt="DOJ files reveal [description]" loading="lazy">
        </a>
        <div class="article-title-section">
            <div class="article-meta">
                <div class="article-tags">
                    <a href="?search=firstname+lastname" class="article-tag">Firstname Lastname</a>
                </div>
                <time datetime="YYYY-MM-DD" class="article-date">Month DD, YYYY</time>
                <span class="reading-time">· X min read</span>
            </div>
            <h2><a href="firstname-lastname-topic.html">[Headline]</a></h2>
            <p class="lede">[Lede text - 1-2 sentences]</p>
            <a href="firstname-lastname-topic.html" class="read-more">Read full article</a>
        </div>
    </div>
</article>
```

**TAG RULES:**
- `data-tags` attribute: Use lowercase full name with space (e.g., `data-tags="woody allen"`)
- Visible tag: Use proper capitalization (e.g., `Woody Allen`)
- Search href: Use `+` for spaces (e.g., `?search=woody+allen`)
- **ONLY use individual FULL names** - NO last names only, NO company names, NO country names

#### 7b. Add to feed.xml

Add new `<item>` with RFC 822 date format.

#### 7c. Update covered-topics.md

Add the new topic to prevent duplicates.

### Step 8: Verify and Publish

**Before committing, run ALL these verification checks:**

```bash
# 1. Thumbnail exists
ls images/firstname-lastname-topic.png

# 2. Article exists
ls firstname-lastname-topic.html

# 3. Article has theme toggle (MUST return 6)
grep -c "theme-toggle" firstname-lastname-topic.html

# 4. Article has dark theme CSS
grep -c "var(--bg)" firstname-lastname-topic.html

# 5. Article has correct branding (should show "Epstein Files Daily")
grep "Epstein Files Daily" firstname-lastname-topic.html | head -1

# 6. index.html has the article card with <img> tag
grep "firstname-lastname-topic.png" index.html
```

**If any check fails, DO NOT commit. Fix the issue first.**

**Commit with ALL files:**
```bash
git add firstname-lastname-topic.html index.html feed.xml images/firstname-lastname-topic.png .skills/epstein-article-generator/references/covered-topics.md
git commit -m "Add article: [headline]"
git push
```

---

## References

- `references/article-template.html` - HTML template (dark theme with light/dark toggle)
- `references/covered-topics.md` - Previously published topics
- `references/create_thumbnail.py` - Thumbnail generator script

## Summary of Key Rules

1. **TEMPLATE IS MANDATORY**: ALWAYS copy `references/article-template.html` - NEVER write HTML from scratch
2. **Verify before publishing**: Article must have theme-toggle (grep returns 6), dark theme CSS, correct branding
3. **Sources**: ONLY use DOJ sources (justice.gov/epstein) - NO external news
4. **Thumbnails**: MANDATORY - Choose appropriate style based on source material:
   - 📧 Email: correspondence, memos
   - ✈️ Flight Log: travel records, passenger lists
   - 💰 Wire Transfer: financial records, payments
   - 📅 Calendar: meetings, appointments, dinners
   - 💬 Text Message: chat logs, informal communications
5. **Tags**: FULL names only (e.g., "woody allen" not "allen"), NO company/country names
6. **Article cards**: MUST include `<img>` thumbnail tag
7. **og:image**: Point to `https://epsteinfilesdaily.com/images/[thumbnail].png`

## Quick Verification Commands

```bash
# Run these BEFORE every commit:
grep -c "theme-toggle" article.html        # Must return 6
grep -c "var(--bg)" article.html           # Must return >0
grep "Epstein Files Daily" article.html    # Must show matches
ls images/thumbnail.png                     # Must exist
```
