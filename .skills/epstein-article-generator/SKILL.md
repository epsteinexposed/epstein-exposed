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

Create a thumbnail image for EVERY article using this exact Python code:

```python
from PIL import Image, ImageDraw, ImageFont
import os

def create_thumbnail(filename, doc_id, to_field, from_field, date_field, highlight_text):
    """
    Create DOJ document-style thumbnail.

    Args:
        filename: Output filename (e.g., "woody-allen-dinners.png")
        doc_id: DOJ document ID (e.g., "EFTA00847392.pdf")
        to_field: Email "To" field
        from_field: Email "From" field
        date_field: Email date
        highlight_text: Key damning quote to highlight
    """
    WIDTH, HEIGHT = 1200, 630
    img = Image.new('RGB', (WIDTH, HEIGHT), (250, 250, 247))
    draw = ImageDraw.Draw(img)

    # Load fonts - LARGE sizes for readability
    try:
        font_header = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_label = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 32)
        font_value = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
        font_highlight = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38)
    except:
        font_header = font_label = font_value = font_highlight = ImageFont.load_default()

    # Dark slate header bar
    draw.rectangle([(0, 0), (WIDTH, 50)], fill=(51, 65, 85))
    draw.text((20, 12), f"📁 DOJ EPSTEIN FILES — {doc_id}", font=font_header, fill=(255, 255, 255))

    # Red accent bar on left (below header)
    draw.rectangle([(0, 50), (18, HEIGHT)], fill=(220, 38, 38))

    # Email metadata - larger spacing
    y = 95
    label_color = (120, 120, 120)
    value_color = (40, 40, 40)

    draw.text((55, y), "To:", font=font_label, fill=label_color)
    draw.text((160, y), to_field, font=font_value, fill=value_color)
    y += 50

    draw.text((55, y), "From:", font=font_label, fill=label_color)
    draw.text((160, y), from_field, font=font_value, fill=value_color)
    y += 50

    draw.text((55, y), "Date:", font=font_label, fill=label_color)
    draw.text((160, y), date_field, font=font_value, fill=value_color)
    y += 70

    # Word wrap the highlight text
    max_width = WIDTH - 120
    words = highlight_text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        test_bbox = draw.textbbox((0, 0), test_line, font=font_highlight)
        if test_bbox[2] - test_bbox[0] > max_width:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))

    # Draw highlighted text with yellow background
    for line in lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_highlight)
        line_width = line_bbox[2] - line_bbox[0]
        line_height = line_bbox[3] - line_bbox[1]
        draw.rectangle([(50, y - 5), (60 + line_width, y + line_height + 10)], fill=(255, 247, 140))
        draw.text((55, y), line, font=font_highlight, fill=(40, 40, 40))
        y += line_height + 22

    # Save to images folder
    os.makedirs("images", exist_ok=True)
    output_path = f"images/{filename}"
    img.save(output_path, 'PNG', quality=95)
    print(f"Created thumbnail: {output_path}")
    return output_path

# USAGE - Run this for each new article:
create_thumbnail(
    filename="firstname-lastname-topic.png",
    doc_id="EFTA00XXXXXX.pdf",
    to_field="Jeffrey Epstein",
    from_field="Person Name",
    date_field="Month DD, YYYY",
    highlight_text="The key damning quote from the document goes here."
)
```

**Thumbnail filename format**: `firstname-lastname-topic.png` (lowercase, hyphens)

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
4. **Thumbnails**: MANDATORY for every article - cream background, DOJ document style, red accent bar
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
