"""Build the Notes section (newsletter archive) from tools/notes/issues/*.txt.

Usage, from the repo root:
    python3 tools/notes/build.py

Writes notes/index.html, one notes/<slug>.html per issue, and the Notes
block of sitemap.xml. The site header and footer are copied from faqs.html,
so re-running picks up any nav or footer changes made there.

Issue file format: "key: value" lines, a line containing only "---", then
the body. Paragraphs are separated by blank lines; consecutive lines
starting with "1. ", "2. " ... become a numbered list. The final two
paragraphs are treated as the sign-off ("Take gentle care," / "JM").
"""

import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
ISSUES = ROOT / "tools" / "notes" / "issues"
OUT = ROOT / "notes"
SITE = "https://anomalytherapy.com"
OG_IMAGE = f"{SITE}/images/logo/og-image.jpg"

AUTHOR = {
    "name": "Jess Mansell",
    "credential": "LPC-MHSP",
    "role": "Founder, Anomaly Therapy",
    "url": "/jess-mansell",
}

INDEX_TITLE = "Notes on Anxiety, Perfectionism & High Performance | Anomaly Therapy"
INDEX_DESCRIPTION = (
    "Notes is the weekly newsletter from Anomaly Therapy in Nashville: short letters "
    "on identity, perfectionism, anxiety, and self-trust for people who carry a lot."
)

esc = html.escape


def parse_issue(path):
    meta_text, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = {}
    for line in meta_text.strip().splitlines():
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    meta["number"] = int(meta["number"])
    meta["date"] = datetime.date.fromisoformat(meta["date"])
    related_href, related_label = (s.strip() for s in meta["related"].split("|", 1))
    meta["related"] = (related_href, related_label)
    meta["blocks"] = [b.strip() for b in body.strip().split("\n\n") if b.strip()]
    meta["url"] = f"/notes/{meta['slug']}"
    return meta


def issue_label(n):
    return f"Newsletter — Issue {n:02d}"


def long_date(d):
    return f"{d:%B} {d.day}, {d.year}"


def render_body(blocks):
    *paragraphs, closing, initials = blocks
    out = []
    for block in paragraphs:
        lines = block.splitlines()
        if all(re.match(r"\d+\.\s", line) for line in lines):
            texts = [re.sub(r"^\d+\.\s+", "", line) for line in lines]
            items = "".join(f"<li>{esc(t)}</li>" for t in texts)
            out.append(f"<ol>{items}</ol>")
        else:
            out.append(f"<p>{'<br />'.join(esc(line) for line in lines)}</p>")
    out.append(
        f'<p class="note__signoff">{esc(closing)}<br /><span>{esc(initials)}</span></p>'
    )
    return "\n          ".join(out)


def chrome():
    """Header and footer markup shared with the rest of the site."""
    source = (ROOT / "faqs.html").read_text(encoding="utf-8")
    top = source[source.index("<body>"):source.index("<main>")]
    bottom = source[source.index("</main>") + len("</main>"):]
    bottom = bottom.replace(
        '<div class="footer__newsletter">',
        '<div class="footer__newsletter" id="subscribe">',
        1,
    )
    return top, bottom


def head(title, description, canonical, og_type, og_title, schema):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}" />
  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#F5F1EA" />
  <!-- Open Graph -->
  <meta property="og:title" content="{esc(og_title)}" />
  <meta property="og:description" content="{esc(description)}" />
  <meta property="og:type" content="{og_type}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{OG_IMAGE}" />
  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(og_title)}" />
  <meta name="twitter:description" content="{esc(description)}" />
  <meta name="twitter:image" content="{OG_IMAGE}" />
  <!-- Favicons -->
  <link rel="icon" type="image/svg+xml" href="/images/logo/monogram.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png" />
  <link rel="icon" href="/favicon.ico" sizes="any" />
  <link rel="apple-touch-icon" href="/apple-touch-icon.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;1,9..144,300;1,9..144,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="/css/style.css" />
  <script type="application/ld+json">
{json.dumps(schema, indent=2, ensure_ascii=False)}
  </script>
</head>
"""


def author_schema():
    return {
        "@type": "Person",
        "name": AUTHOR["name"],
        "honorificSuffix": AUTHOR["credential"],
        "jobTitle": AUTHOR["role"],
        "url": SITE + AUTHOR["url"],
    }


PUBLISHER = {
    "@type": "Organization",
    "name": "Anomaly Therapy",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": OG_IMAGE},
}


def issue_page(issue, prev_issue, next_issue, top, bottom):
    canonical = SITE + issue["url"]
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": issue["title"],
        "description": issue["description"],
        "datePublished": issue["date"].isoformat(),
        "author": author_schema(),
        "publisher": PUBLISHER,
        "mainEntityOfPage": canonical,
        "image": OG_IMAGE,
        "isPartOf": {"@type": "Blog", "name": "Notes", "url": SITE + "/notes/"},
    }
    related_href, related_label = issue["related"]

    pager = []
    if prev_issue:
        pager.append(
            f'<a class="note-pager__link" href="{prev_issue["url"]}" rel="prev">'
            f'<span class="note-pager__dir">← Previous</span>'
            f'<span class="note-pager__title">{esc(prev_issue["title"])}</span></a>'
        )
    else:
        pager.append("<span></span>")
    if next_issue:
        pager.append(
            f'<a class="note-pager__link note-pager__link--next" href="{next_issue["url"]}" rel="next">'
            f'<span class="note-pager__dir">Next →</span>'
            f'<span class="note-pager__title">{esc(next_issue["title"])}</span></a>'
        )

    main = f"""<main>

    <article class="note">
      <header class="page-head note__head">
        <div class="container container--text">
          <p class="note__kicker"><a href="/notes/">Notes</a> <span aria-hidden="true">·</span> {issue_label(issue["number"])}</p>
          <h1 class="page-head__title note__title">{esc(issue["title"])}</h1>
          <p class="page-head__sub">{esc(issue["dek"])}</p>
          <p class="note__byline">By <a href="{AUTHOR["url"]}">{AUTHOR["name"]}, {AUTHOR["credential"]}</a> <span aria-hidden="true">·</span> <time datetime="{issue["date"].isoformat()}">{long_date(issue["date"])}</time></p>
        </div>
      </header>

      <div class="section section--tight">
        <div class="container container--text note__body">
          {render_body(issue["blocks"])}
        </div>
      </div>

      <aside class="section section--tight note__end" aria-label="About this newsletter">
        <div class="container container--text">
          <div class="note-author">
            <p class="eyebrow eyebrow--muted">Written by</p>
            <p class="note-author__name"><a href="{AUTHOR["url"]}">{AUTHOR["name"]}, {AUTHOR["credential"]}</a></p>
            <p class="note-author__bio">{AUTHOR["role"]}. Jess works with executives, high performing professionals, and couples in Nashville.</p>
          </div>
          <div class="note-cta">
            <p>Notes arrives every Tuesday morning. <a class="tlink" href="#subscribe">Get the next issue by email</a></p>
            <p><a class="tlink" href="{related_href}">{esc(related_label)}</a></p>
          </div>
          <nav class="note-pager" aria-label="More issues">
            {"".join(pager)}
          </nav>
        </div>
      </aside>
    </article>

  </main>"""
    return head(
        issue["seo_title"], issue["description"], canonical, "article",
        issue["title"], schema,
    ) + top + main + bottom


def index_page(issues, top, bottom):
    canonical = SITE + "/notes/"
    schema = {
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "Notes",
        "description": INDEX_DESCRIPTION,
        "url": canonical,
        "publisher": PUBLISHER,
        "blogPost": [
            {
                "@type": "BlogPosting",
                "headline": i["title"],
                "url": SITE + i["url"],
                "datePublished": i["date"].isoformat(),
                "author": author_schema(),
            }
            for i in issues
        ],
    }
    cards = "\n".join(
        f"""          <li class="note-list__item">
            <a class="note-list__link" href="{i["url"]}">
              <span class="note-list__meta">{issue_label(i["number"])} <span aria-hidden="true">·</span> <time datetime="{i["date"].isoformat()}">{long_date(i["date"])}</time></span>
              <span class="note-list__title">{esc(i["title"])}</span>
              <span class="note-list__dek">{esc(i["dek"])}</span>
            </a>
          </li>"""
        for i in issues
    )
    main = f"""<main>

    <section class="page-head">
      <div class="container">
        <p class="eyebrow mb-2">Notes · Every Tuesday</p>
        <h1 class="page-head__title">
          Notes from <em class="italic">underneath</em> the performance.
        </h1>
        <p class="page-head__sub">
          A weekly letter from {AUTHOR["name"]}, founder of Anomaly, on identity, perfectionism, anxiety, and self-trust, for people who carry a lot. Read past issues below, or <a href="#subscribe" style="color: inherit; text-decoration: underline; text-underline-offset: 3px;">subscribe</a> to get them first.
        </p>
      </div>
    </section>

    <section class="section">
      <div class="container container--text">
        <ol class="note-list" reversed>
{cards}
        </ol>
      </div>
    </section>

  </main>"""
    return head(
        INDEX_TITLE, INDEX_DESCRIPTION, canonical, "website",
        "Notes — Anomaly Therapy", schema,
    ) + top + main + bottom


def update_sitemap(issues):
    path = ROOT / "sitemap.xml"
    sitemap = path.read_text(encoding="utf-8")
    entries = [
        ("/notes/", issues[0]["date"], "weekly", "0.7")
    ] + [(i["url"], i["date"], "yearly", "0.6") for i in issues]
    block = "  <!-- notes:start (generated by tools/notes/build.py) -->\n" + "".join(
        f"  <url>\n    <loc>{SITE}{loc}</loc>\n    <lastmod>{d.isoformat()}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>\n"
        for loc, d, freq, prio in entries
    ) + "  <!-- notes:end -->\n"
    pattern = re.compile(r"  <!-- notes:start.*?<!-- notes:end -->\n", re.S)
    if pattern.search(sitemap):
        sitemap = pattern.sub(lambda _: block, sitemap)
    else:
        sitemap = sitemap.replace("</urlset>", block + "</urlset>")
    path.write_text(sitemap, encoding="utf-8")


def main():
    issues = sorted(
        (parse_issue(p) for p in ISSUES.glob("*.txt")),
        key=lambda i: i["number"],
        reverse=True,
    )
    top, bottom = chrome()
    OUT.mkdir(exist_ok=True)
    for idx, issue in enumerate(issues):
        newer = issues[idx - 1] if idx > 0 else None
        older = issues[idx + 1] if idx + 1 < len(issues) else None
        (OUT / f"{issue['slug']}.html").write_text(
            issue_page(issue, older, newer, top, bottom), encoding="utf-8"
        )
    (OUT / "index.html").write_text(index_page(issues, top, bottom), encoding="utf-8")
    update_sitemap(issues)
    print(f"Built {len(issues)} issues + index into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
