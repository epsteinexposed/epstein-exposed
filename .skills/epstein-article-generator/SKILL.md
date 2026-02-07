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

**DEFAULT STYLE: Authentic Leaked Email**

All thumbnails should look like actual leaked DOJ email screenshots with:
- Plain white background
- Email headers (To/From/Sent/Subject) with full email addresses
- Yellow highlight on incriminating text
- "Sent from my BlackBerry®" signature
- Dark navy DOJ bar at bottom with document number

**Thumbnail filename format**: `firstname-lastname-topic.png` (lowercase, hyphens)

---

#### 📧 AUTHENTIC EMAIL THUMBNAIL (Use for ALL articles)

```python
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

# Usage:
create_authentic_email(
    "images/person-topic.png",
    to_email="Jeffrey Epstein[jeevacation@gmail.com]",
    from_email="Person Name[person@email.com]",
    sent_date="Thur 3/15/2005 2:30:15 PM",
    subject="Re: Meeting Request",
    body_lines=[
        "Looking forward to our meeting",
        "at the island next week.",
        "",
        "Keep this between us."
    ],
    highlight_text="between us",
    doc_number="DOJ-EPSTEIN-004521"
)
```

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
4. **Thumbnails**: MANDATORY - Use the authentic leaked email style (yellow highlights, BlackBerry signature, dark navy DOJ bar)
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
