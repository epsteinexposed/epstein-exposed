---
name: epstein-article-generator
description: |
  Generate new articles for Epstein Exposed website based on DOJ document releases.
  TRIGGERS: "write new article", "generate article", "publish article", "daily article", "epstein article"
  Finds interesting DOJ documents, writes SEO-optimized investigative articles, updates the site, and pushes to GitHub.
---

# Epstein Article Generator

Generate investigative journalism articles for epstein-exposed.com based on DOJ file releases.

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

- Only use real DOJ document IDs (format: EFTAxxxxxxxx.pdf)
- Verify URLs exist at justice.gov
- Quote directly from documents

### Step 4: Write Article

Use template from `references/article-template.html`. Elements:

**Headline**: Attention-grabbing, uses quotes from docs when possible
**Lede**: 1-2 sentence hook summarizing the revelation
**Body**:
1. Opening context (2-3 paragraphs)
2. Document evidence box with DOJ source
3. Additional context/analysis
4. Response box (or note if no response)
5. Source box with DOJ links
6. Share buttons

**SEO**: Title <60 chars, meta description 150-160 chars, full name in title/first paragraph

**Style**: Tabloid tone but factual, short paragraphs, pull quotes for damning evidence

### Step 5: Save Article

Save HTML to workspace: `topic-key-detail.html` (lowercase, hyphens)

### Step 6: Update Site

1. Add article card to `index.html`
2. Add `<item>` to `feed.xml` (RFC 822 date format)
3. Update `references/covered-topics.md`

### Step 7: Publish

```bash
git add [article].html index.html feed.xml
git commit -m "Add article: [headline]"
git push
```

## References

- `references/article-template.html` - HTML template
- `references/covered-topics.md` - Previously published topics
