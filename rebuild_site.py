#!/usr/bin/env python3
"""Rebuild monetize-site from scratch. Clean HTML, proper SEO, no duplicates."""
import os, re

SITE_DIR = "/data/data/com.termux/files/home/monetize-site"
ARTICLES_DIR = os.path.join(SITE_DIR, "articles")

ARTICLES = [
    {
        "title": "Apple and Google Crush California Bill to Aid Smaller Rivals: Implications and Insights",
        "desc": "Explore how Apple and Google crushed the California bill that aimed to support smaller rivals in the tech industry.",
        "slug": "apple-google-california-bill-smaller-rivals",
        "date": "2026-05-10", "category": "Tech Policy",
        "source_md": "apple-google-california-bill-smaller-rivals.md",
    },
    {
        "title": "Claude-Powered AI Coding Agent Deletes Entire Company Database in 9 Seconds: A Cautionary Tale",
        "desc": "A shocking incident where a Claude-powered AI coding agent deleted an entire company database in just 9 seconds.",
        "slug": "claude-ai-coding-agent-deletes-database",
        "date": "2026-05-09", "category": "AI Safety",
        "source_md": "claude-ai-coding-agent-deletes-database.md",
    },
    {
        "title": "DeepSeek-V4 Arrives with Near State-of-the-Art Intelligence at 1/6th the Cost of Competitors",
        "desc": "Discover how DeepSeek-V4 delivers near state-of-the-art AI intelligence at 1/6th the cost of competitors.",
        "slug": "deepseek-v4-arrives-with-near-state-of-the-art-intelligence-at-1-6th-the-cost-of",
        "date": "2026-05-08", "category": "AI Models",
        "source_md": "deepseek-v4-arrives-with-near-state-of-the-art-intelligence-at-1-6th-the-cost-of.md",
    },
    {
        "title": "The Foldable iPhone: Is It Really Just an iPad Mini That Folds in Half?",
        "desc": "Discover how the foldable iPhone is essentially an iPad Mini that folds in half.",
        "slug": "foldable-iphone-ipad-mini",
        "date": "2026-05-07", "category": "Apple",
        "source_md": "** foldable-iphone-ipad-mini.md",
    },
    {
        "title": "Microsoft VibeVoice: Open-Source Frontier Voice AI – A Comprehensive Guide",
        "desc": "Discover Microsoft VibeVoice, an open-source frontier voice AI framework.",
        "slug": "microsoft-vibevoice-open-source-frontier-voice-ai",
        "date": "2026-05-06", "category": "Voice AI",
        "source_html": "microsoft-vibevoice-open-source-frontier-voice-ai.html",
    },
    {
        "title": "Show HN: Live Sun and Moon Dashboard with NASA Footage - A Comprehensive Guide",
        "desc": "Discover the Live Sun and Moon Dashboard with NASA Footage.",
        "slug": "show-hn-live-sun-moon-dashboard-nasa-footage-guide",
        "date": "2026-05-05", "category": "Open Source",
        "source_html": "show-hn-live-sun-moon-dashboard-nasa-footage-guide.html",
    },
    {
        "title": "I Forked a 140k+ Star AI Project and Customized It for Android — Here's Everything I Changed",
        "desc": "How I customized NousResearch/hermes-agent for Termux ARM64 — the full technical breakdown of ARM64 compat, venv fixes, Python 3.12 patches, and more.",
        "slug": "fork-customization-post",
        "date": "2026-05-11", "category": "AI Automation",
        "source_md": "fork-customization-post.md",
    },
]

CSS = """    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.7; color: #333; background: #f5f5f5; }
    header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2.5rem 1rem; text-align: center; }
    header h1 { font-size: 2.2rem; margin-bottom: 0.5rem; }
    header p { opacity: 0.9; font-size: 1.1rem; }
    nav { background: white; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
    nav a { color: #667eea; text-decoration: none; margin: 0 1rem; font-weight: 500; }
    nav a:hover { text-decoration: underline; }
    .container { max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
    .article-card { background: white; padding: 1.5rem; margin-bottom: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s; }
    .article-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
    .article-card h2 { margin-bottom: 0.3rem; font-size: 1.2rem; }
    .article-card h2 a { color: #333; text-decoration: none; }
    .article-card h2 a:hover { color: #667eea; }
    .article-card .meta { color: #888; font-size: 0.85rem; margin-bottom: 0.5rem; }
    .article-card .category { display: inline-block; background: #667eea; color: white; padding: 0.15rem 0.5rem; border-radius: 3px; font-size: 0.75rem; margin-right: 0.5rem; }
    .content { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .content h1 { color: #333; margin-bottom: 0.5rem; font-size: 1.8rem; }
    .content h2 { color: #444; margin-top: 2rem; margin-bottom: 1rem; font-size: 1.4rem; }
    .content h3 { color: #555; margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.15rem; }
    .content p { margin-bottom: 1rem; }
    .content ul, .content ol { margin-left: 2rem; margin-bottom: 1rem; }
    .content li { margin-bottom: 0.3rem; }
    .content blockquote { border-left: 4px solid #667eea; padding-left: 1rem; margin: 1rem 0; color: #555; font-style: italic; }
    .content code { background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; font-size: 0.9rem; }
    .content pre { background: #f4f4f4; padding: 1rem; border-radius: 5px; overflow-x: auto; margin-bottom: 1rem; }
    .content pre code { background: none; padding: 0; }
    .affiliate-box { background: #fff8e1; border: 1px solid #ffc107; padding: 1rem 1.5rem; border-radius: 8px; margin: 1.5rem 0; }
    .affiliate-box h4 { color: #856404; margin-bottom: 0.5rem; }
    .affiliate-box a { color: #856404; font-weight: bold; }
    .affiliate-box ul { margin-left: 1.5rem; }
    .article-meta { color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; padding-bottom: 1rem; border-bottom: 1px solid #eee; }
    footer { background: #333; color: white; text-align: center; padding: 2rem; margin-top: 3rem; }
    footer p { margin-bottom: 0.3rem; }
    footer a { color: #aaa; }
    @media (max-width: 600px) {
        header h1 { font-size: 1.6rem; }
        .content { padding: 1.5rem; }
        .content h1 { font-size: 1.4rem; }
    }"""


def html_page(title, desc, content):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | AI Tech News</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://alaamohanad169-ship-it.github.io/monetize-site/">
  <style>{CSS}</style>
</head>
<body>
  <header>
    <h1>🚀 AI Tech News</h1>
    <p>Latest insights on AI, tech trends, and digital innovation</p>
  </header>
  <nav>
    <a href="/">Home</a>
    <a href="/#articles">Articles</a>
    <a href="/#about">About</a>
    <a href="/#contact">Contact</a>
  </nav>
  <div class="container">
{content}
  </div>
  <footer>
    <p>&copy; 2026 AI Tech News. All rights reserved.</p>
    <p style="font-size:0.8rem;margin-top:0.5rem;">Some links are affiliate links — we may earn a commission at no extra cost to you.</p>
  </footer>
</body>
</html>"""


def md_to_html(md_text):
    """Convert markdown to clean HTML."""
    text = md_text
    # Remove YAML frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    # Remove TITLE/META/KEYWORDS/SLUG lines
    text = re.sub(r'^(TITLE|META|KEYWORDS|SLUG):\s*.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^-{3,}\s*$', '', text, flags=re.MULTILINE)

    # Headers (h6 first down to h1)
    for i in range(6, 0, -1):
        text = re.sub(r'^#{%d}\s+(.+)$' % i, r'<h%d>\1</h%d>' % (i, i), text, flags=re.MULTILINE)

    # Bold, italic, code, links
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'```\w*\n(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # Blockquotes: remove affiliate-style "> Recommended:" lines, keep real blockquotes
    def bq(m):
        c = m.group(1)
        if 'Recommended:' in c or 'amzn.to' in c:
            return ''
        return f'<blockquote>{c}</blockquote>'
    text = re.sub(r'^>\s+(.+)$', bq, text, flags=re.MULTILINE)

    # Unordered lists
    def convert_ul(m):
        items = re.sub(r'^- (.+)$', r'<li>\1</li>', m.group(0), flags=re.MULTILINE)
        items = re.sub(r'^\s+- (.+)$', r'<li>\1</li>', items, flags=re.MULTILINE)
        return f'<ul>{items}</ul>'
    text = re.sub(r'(?:^- .+\n?)+', convert_ul, text, flags=re.MULTILINE)

    # Ordered lists
    def convert_ol(m):
        items = re.sub(r'^\d+\.\s+(.+)$', r'<li>\1</li>', m.group(0), flags=re.MULTILINE)
        return f'<ol>{items}</ol>'
    text = re.sub(r'(?:^\d+\..+\n?)+', convert_ol, text, flags=re.MULTILINE)

    # Wrap plain text in <p>
    lines = text.split('\n')
    result = []
    for line in lines:
        s = line.strip()
        if not s:
            result.append('')
            continue
        if s.startswith('<'):
            result.append(s)
        else:
            result.append(f'<p>{s}</p>')
    text = '\n'.join(result)
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Remove the first <h1> (page template already has one)
    text = re.sub(r'^\s*<h1>.*?</h1>\s*', '', text, count=1, flags=re.DOTALL)

    # Remove stray backticks
    text = re.sub(r'<p>```</p>', '', text)
    text = re.sub(r'```', '', text)

    return text.strip()


def extract_body_from_old_html(html_path):
    """Extract article body from old HTML files."""
    with open(html_path, 'r') as f:
        content = f.read()

    match = re.search(r'<div class="content">(.*?)</div>\s*</div>\s*<footer>', content, re.DOTALL)
    if not match:
        return None

    inner = match.group(1)

    # Remove everything before the first <h1>
    h1_match = re.search(r'<h1>', inner)
    if h1_match:
        inner = inner[h1_match.start():]

    # Remove affiliate-style paragraphs
    inner = re.sub(r'<p>>\s*<strong>Recommended:</strong>.*?</p>', '', inner, flags=re.DOTALL)
    inner = re.sub(r'<blockquote><strong>Recommended:</strong>.*?</blockquote>', '', inner, flags=re.DOTALL)

    # Remove duplicate h1 tags (keep first)
    h1_tags = list(re.finditer(r'<h1>.*?</h1>', inner, re.DOTALL))
    if len(h1_tags) > 1:
        for extra in reversed(h1_tags[1:]):
            inner = inner[:extra.start()] + inner[extra.end():]

    # Remove META/KEYWORDS/SLUG/---
    inner = re.sub(r'<p>\s*(TITLE|META|KEYWORDS|SLUG|---)\s*:.*?</p>', '', inner, flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(r'<p><strong>(META|KEYWORDS|SLUG)</strong>:.*?</p>', '', inner, flags=re.DOTALL | re.IGNORECASE)

    # Remove <pre><code>markdown wrapper
    inner = re.sub(r'<p><pre><code>markdown\s*\n?', '', inner)
    inner = re.sub(r'</code></pre></p>', '', inner)

    # Remove <p> wrapping block elements
    for tag in ['h1','h2','h3','h4','h5','h6','ul','ol','blockquote','pre','div']:
        inner = re.sub(r'<p>(<' + tag + r'>)', r'\1', inner)
        inner = re.sub(r'(</' + tag + r'>)</p>', r'\1', inner)

    # Remove empty code tags and backticks
    inner = re.sub(r'<p><code></code>`</p>', '', inner)
    inner = re.sub(r'<code></code>`', '', inner)

    # Remove duplicate article-meta divs
    meta_matches = list(re.finditer(r'<div class="article-meta">.*?</div>', inner, re.DOTALL))
    if len(meta_matches) > 1:
        for extra in reversed(meta_matches[1:]):
            inner = inner[:extra.start()] + inner[extra.end():]

    # Remove existing affiliate-box divs
    inner = re.sub(r'<div class="affiliate-box">.*?</div>', '', inner, flags=re.DOTALL)

    # Remove the first <h1> (page template already has one)
    inner = re.sub(r'^\s*<h1>.*?</h1>\s*', '', inner, count=1, flags=re.DOTALL)

    # Remove stray backticks
    inner = re.sub(r'<p>```</p>', '', inner)
    inner = re.sub(r'```', '', inner)

    return inner.strip()


def affiliate_box():
    return """
    <div class="affiliate-box">
      <h4>🛒 Recommended Gear for Tech Enthusiasts</h4>
      <ul>
        <li><a href="https://amzn.to/3SonyXM5" target="_blank" rel="nofollow noopener">Sony WH-1000XM5</a> — Best noise-cancelling headphones for focused work.</li>
        <li><a href="https://amzn.to/3DellXPS15" target="_blank" rel="nofollow noopener">Dell XPS 15</a> — Premium Windows laptop for developers and creators.</li>
        <li><a href="https://amzn.to/3MacBookPro" target="_blank" rel="nofollow noopener">MacBook Pro</a> — Best laptop for developers and power users.</li>
      </ul>
      <p style="font-size:0.8rem;color:#856404;margin-top:0.5rem;">As an Amazon Associate, we earn from qualifying purchases.</p>
    </div>"""


def build_article(article, body_html):
    return f"""    <div class="content">
      <div class="article-meta">
        <span class="category">{article['category']}</span> &middot; {article['date']}
      </div>
      <h1>{article['title']}</h1>
      {body_html}
      {affiliate_box()}
    </div>"""


def build_index(articles):
    cards = []
    for a in articles:
        cards.append(f"""    <div class="article-card">
      <h2><a href="articles/{a['slug']}.html">{a['title']}</a></h2>
      <div class="meta"><span class="category">{a['category']}</span> &middot; {a['date']}</div>
      <p>{a['desc']}</p>
    </div>""")

    content = f"""    <h2 id="articles" style="margin-bottom:1.5rem;">📰 Latest Articles</h2>
{''.join(cards)}

    <div id="about" style="margin-top:3rem;padding:2rem;background:white;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
      <h2>About AI Tech News</h2>
      <p style="margin-top:1rem;">We cover the latest in artificial intelligence, tech trends, and digital innovation. Our mission is to make complex tech topics accessible to everyone.</p>
    </div>

    <div id="contact" style="margin-top:2rem;padding:2rem;background:white;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,0.1);">
      <h2>Contact</h2>
      <p style="margin-top:1rem;">Email: <a href="mailto:contact@aitechnews.com">contact@aitechnews.com</a></p>
    </div>"""

    return html_page(
        "AI Tech News — Latest AI & Tech Insights",
        "Latest news and insights on AI, tech trends, and digital innovation.",
        content
    )


def main():
    os.makedirs(ARTICLES_DIR, exist_ok=True)

    for article in ARTICLES:
        slug = article["slug"]
        html_path = os.path.join(ARTICLES_DIR, f"{slug}.html")
        body = None

        # Try markdown source first
        if article.get("source_md"):
            md_path = os.path.join(SITE_DIR, article["source_md"])
            if os.path.exists(md_path):
                with open(md_path, 'r') as f:
                    body = md_to_html(f.read())

        # Try HTML source
        if not body and article.get("source_html"):
            html_source = os.path.join(ARTICLES_DIR, article["source_html"])
            if os.path.exists(html_source):
                body = extract_body_from_old_html(html_source)

        if not body:
            body = "<p>Article content coming soon.</p>"

        page = html_page(article["title"], article["desc"], build_article(article, body))
        with open(html_path, 'w') as f:
            f.write(page)
        print(f"  ✓ {slug}.html")

    # Build index
    with open(os.path.join(SITE_DIR, "index.html"), 'w') as f:
        f.write(build_index(ARTICLES))
    print(f"  ✓ index.html")

    # Clean up root .md files (duplicates — content is now in HTML)
    for f in os.listdir(SITE_DIR):
        if f.endswith('.md') and f not in ['README.md']:
            os.remove(os.path.join(SITE_DIR, f))
            print(f"  ✗ Removed root {f}")

    # Clean up duplicate HTML files in articles/
    for dup in ['claude-ai-database-deletion.html', 'deepseek-v4-intelligence-cost.html']:
        p = os.path.join(ARTICLES_DIR, dup)
        if os.path.exists(p):
            os.remove(p)
            print(f"  ✗ Removed duplicate {dup}")

    print(f"\n✅ Done: {len(ARTICLES)} articles + index")


if __name__ == "__main__":
    main()
