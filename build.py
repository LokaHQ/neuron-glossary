#!/usr/bin/env python3
"""Build the Neuron Glossary into a single self-contained index.html.

Reads `glossary/<section>/<term>.md`, renders it, and emits one HTML file with
inline CSS/JS and inlined SVG diagrams — no build step and no network needed to
read the result.

All prose lives in Markdown. Nothing in this file is content; `index.html` is a
pure build artifact and is fully reproducible from `glossary/`.

Usage:
    python3 build.py [--out index.html] [--check]
"""

import argparse
import html
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "utils"))

from render import parse_frontmatter, render_markdown, strip_markdown  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
GLOSSARY = os.path.join(ROOT, "glossary")
DIAGRAMS = os.path.join(ROOT, "assets", "diagrams")
HOME_INDEX = os.path.join(GLOSSARY, "index.md")
ASCII_ART = os.path.join(ROOT, "assets", "loka-wordmark.txt")
SHARE_IMAGE = "assets/neuron-glossary-og.png"
SHARE_SIZE = (1200, 630)

SITE_URL = "https://lokahq.github.io/neuron-glossary/"
SECTION_ORDER = ["device-hardware", "device-software", "host-software", "perf"]
LINK_PREFIX = "/neuron-glossary/"


class BuildError(Exception):
    """Raised when the source tree is inconsistent enough to abort the build."""


def _read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# --- loading ----------------------------------------------------------------


def load_sections():
    """Load every section and its terms from the glossary tree.

    Returns:
        A list of section dicts, each with `slug`, `title`, `blurb`, and `terms`.

    Raises:
        BuildError: If a section directory or its index file is missing.
    """
    sections = []
    for slug in SECTION_ORDER:
        directory = os.path.join(GLOSSARY, slug)
        index_path = os.path.join(GLOSSARY, f"{slug}.md")
        if not os.path.isdir(directory):
            raise BuildError(f"missing section directory: glossary/{slug}/")
        if not os.path.isfile(index_path):
            raise BuildError(f"missing section index: glossary/{slug}.md")

        meta, body = parse_frontmatter(_read(index_path))
        terms = []
        for name in sorted(os.listdir(directory)):
            if not name.endswith(".md"):
                continue
            term_meta, term_body = parse_frontmatter(_read(os.path.join(directory, name)))
            term_slug = name[:-3]
            title = term_meta.get("title")
            if not title:
                raise BuildError(f"missing `title` in glossary/{slug}/{name}")
            terms.append(
                {
                    "slug": term_slug,
                    "title": title,
                    "short": term_meta.get("short", title),
                    "abbr": term_meta.get("abbr", ""),
                    "body": term_body,
                    "path": f"{slug}/{term_slug}",
                }
            )
        if not terms:
            raise BuildError(f"section has no terms: glossary/{slug}/")
        # Order by the sidebar label, so "NeuronCore" precedes "NeuronCore-v1".
        terms.sort(key=lambda t: t["short"].lower())
        sections.append(
            {
                "slug": slug,
                "title": meta.get("title", slug),
                "blurb": body.strip(),
                "terms": terms,
            }
        )
    return sections


def load_home():
    """Load site metadata and the README body from glossary/index.md."""
    if not os.path.isfile(HOME_INDEX):
        raise BuildError("missing glossary/index.md")
    meta, body = parse_frontmatter(_read(HOME_INDEX))
    for key in ("title", "tagline"):
        if not meta.get(key):
            raise BuildError(f"missing `{key}` in glossary/index.md")
    return meta, body


# --- resolvers --------------------------------------------------------------


def make_link_resolver(known_paths, source, problems):
    """Build a link resolver that rewrites internal glossary links to hash routes."""

    def resolve(href):
        if href.startswith(("http://", "https://", "mailto:")):
            return href, True
        if href.startswith("#"):
            return href, False
        if href.startswith(LINK_PREFIX):
            target = href[len(LINK_PREFIX):].strip("/")
            if target and target not in known_paths:
                problems.append(f"{source}: link to unknown term '{target}'")
            return f"#/{target}", False
        problems.append(f"{source}: unrecognized link '{href}'")
        return href, False

    return resolve


def make_image_resolver(source, problems, used):
    """Build an image resolver that inlines themed SVG diagram pairs."""
    figure_number = 0
    source_id = source.removesuffix(".md").replace("/", "_")

    def resolve(alt, src):
        nonlocal figure_number
        caption = alt.strip()
        if not src.startswith("themed-image://"):
            problems.append(f"{source}: non-themed image '{src}'")
            return ""
        name = src[len("themed-image://"):]
        stem = name[:-4] if name.endswith(".svg") else name
        light = os.path.join(DIAGRAMS, f"{stem}-light.svg")
        dark = os.path.join(DIAGRAMS, f"{stem}-dark.svg")
        if not (os.path.isfile(light) and os.path.isfile(dark)):
            problems.append(f"{source}: missing diagram pair for '{stem}'")
            return ""
        used.add(stem)
        figure_number += 1
        prefix = f"{source_id}-{figure_number}"
        cap = f"<figcaption>{_inline_caption(caption)}</figcaption>" if caption else ""
        decorative = ' aria-hidden="true"' if caption else ""
        return (
            '<figure class="diagram">'
            f'<div class="diagram-light"{decorative}>{_clean_svg(_read(light), prefix + "-light")}</div>'
            f'<div class="diagram-dark"{decorative}>{_clean_svg(_read(dark), prefix + "-dark")}</div>'
            f"{cap}</figure>"
        )

    return resolve


def _clean_svg(text, prefix):
    """Prepare an inline SVG and keep its arrow markers local to the figure."""
    text = re.sub(r"<\?xml[^>]*\?>", "", text)
    text = re.sub(r"<!DOCTYPE[^>]*>", "", text)
    text = re.sub(r'(id="|url\(#)(arrow-[\w-]+)', rf"\g<1>{prefix}-\2", text)
    return text.strip()


def _inline_caption(text):
    """Render the small subset of markdown allowed inside a figure caption."""
    out = html.escape(text)
    out = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
                 r'<a href="\2" target="_blank" rel="noopener">\1</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    return out


# --- fragments --------------------------------------------------------------


def _chip(abbr):
    return f'<span class="chip">{html.escape(abbr)}</span>' if abbr else ""


def _term_link(term):
    """A link to a term, with its abbreviation chip if it has one."""
    return (
        f'<a href="#/{term["path"]}">{html.escape(term["short"])}</a>'
        f'{_chip(term["abbr"])}'
    )


def _crumb(path):
    """The terminal-style path line shown above every heading."""
    return f'<div class="crumb">/{html.escape(path)}</div>'


# --- assembly ---------------------------------------------------------------


def build(out_path, check_only=False):
    """Render the whole site and write it to `out_path`."""
    sections = load_sections()
    home_meta, readme_body = load_home()
    known = {t["path"] for s in sections for t in s["terms"]}
    known |= {s["slug"] for s in sections}
    known.update(("readme", "contributors"))
    problems = []
    used_diagrams = set()

    flat = [t for s in sections for t in s["terms"]]
    order = [t["path"] for t in flat]

    articles = []
    search_index = []
    for section in sections:
        for term in section["terms"]:
            source = f"glossary/{term['path']}.md"
            resolver = make_link_resolver(known, source, problems)
            images = make_image_resolver(source, problems, used_diagrams)
            body_html = render_markdown(term["body"], resolver, images)

            pos = order.index(term["path"])
            articles.append(
                _article(
                    section,
                    term,
                    body_html,
                    flat[pos - 1] if pos > 0 else None,
                    flat[pos + 1] if pos < len(flat) - 1 else None,
                )
            )
            search_index.append(
                {
                    "p": term["path"],
                    "t": term["short"],
                    "a": term["abbr"],
                    "s": section["title"],
                    "b": strip_markdown(term["body"])[:600],
                }
            )

    for section in sections:
        resolver = make_link_resolver(known, f"glossary/{section['slug']}.md", problems)
        section["blurb_html"] = render_markdown(section["blurb"], resolver)

    readme_html = render_markdown(
        readme_body, make_link_resolver(known, "glossary/index.md", problems)
    )
    search_index.append({
        "p": "readme", "t": "README", "a": "", "s": "Home",
        "b": strip_markdown(readme_body)[:600],
    })
    authors = _read(os.path.join(ROOT, "AUTHORS.md")).partition("\n")[2]
    authors_html = render_markdown(
        authors, make_link_resolver(known, "AUTHORS.md", problems)
    )
    search_index.append({
        "p": "contributors", "t": "Contributors", "a": "", "s": "Glossary",
        "b": strip_markdown(authors),
    })

    _warn_unused_diagrams(used_diagrams, problems)
    if check_only:
        try:
            with open(os.path.join(ROOT, SHARE_IMAGE), "rb") as handle:
                header = handle.read(24)
        except OSError as error:
            raise BuildError(f"cannot read share image {SHARE_IMAGE}: {error}") from error
        if (len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR"
                or struct.unpack(">II", header[16:24]) != SHARE_SIZE):
            problems.append(f"{SHARE_IMAGE}: expected a {SHARE_SIZE[0]} × {SHARE_SIZE[1]} PNG")

    if problems:
        for problem in problems:
            print(f"  ! {problem}", file=sys.stderr)
        if check_only:
            raise BuildError(f"{len(problems)} problem(s) found")

    page = _page(sections, articles, search_index, home_meta, readme_html, authors_html)

    if check_only:
        print(f"check ok: {len(flat)} terms, {len(sections)} sections")
        return page

    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(page)
    print(f"wrote {out_path} ({os.path.getsize(out_path) / 1024:.0f} KiB) — "
          f"{len(flat)} terms, {len(sections)} sections")
    return page


def _warn_unused_diagrams(used, problems):
    if not os.path.isdir(DIAGRAMS):
        return
    stems = set()
    for name in os.listdir(DIAGRAMS):
        for suffix in ("-light.svg", "-dark.svg"):
            if name.endswith(suffix):
                stems.add(name[: -len(suffix)])
    for stem in sorted(stems - used):
        problems.append(f"assets/diagrams: '{stem}' is never referenced")


def _article(section, term, body_html, prev_term, next_term):
    nav = []
    for other, direction, arrow in (
        (prev_term, "prev", "&larr;"), (next_term, "next", "&rarr;")
    ):
        if other:
            nav.append(
                f'<a class="pager {direction}" href="#/{other["path"]}">'
                f'<span class="pager-arrow">{arrow}</span>'
                f'<span class="pager-title">{html.escape(other["short"])}</span></a>'
            )
        else:
            nav.append('<span class="pager"></span>')

    return (
        f'<article class="term" data-route="{term["path"]}" hidden>'
        f'{_crumb(term["path"])}'
        f'<h1>{html.escape(term["title"])}{_chip(term["abbr"])}</h1>'
        f'<div class="prose">{body_html}</div>'
        f'<nav class="pagers">{"".join(nav)}</nav>'
        f"</article>"
    )


def _section_page(section):
    items = "".join(f"<li>{_term_link(t)}</li>" for t in section["terms"])
    return (
        f'<article class="term section-page" data-route="{section["slug"]}" hidden>'
        f'{_crumb(section["slug"])}'
        f'<h1>{html.escape(section["title"])}</h1>'
        f'<div class="prose">{section["blurb_html"]}</div>'
        f'<ul class="arrow-list">{items}</ul>'
        f"</article>"
    )


def _readme(sections, tagline, readme_html):
    """Render the glossary introduction and term directory."""
    blocks = []
    for section in sections:
        items = "".join(f"<li>{_term_link(t)}</li>" for t in section["terms"])
        blocks.append(
            f'<section class="readme-section">'
            f'<h2><a href="#/{section["slug"]}">{html.escape(section["title"])}</a></h2>'
            f'<div class="prose readme-blurb">{section["blurb_html"]}</div>'
            f'<ul class="arrow-list readme-list">{items}</ul>'
            f"</section>"
        )
    total = sum(len(s["terms"]) for s in sections)
    return (
        '<article class="term" data-route="readme" hidden>'
        f'{_crumb("readme")}<h1>README</h1>'
        f'<p class="lede">{html.escape(tagline)}</p>'
        f'<div class="prose">{readme_html}</div>'
        f'<p class="count">{total} terms across {len(sections)} sections.</p>'
        f'{"".join(blocks)}'
        "</article>"
    )


# --- page shell -------------------------------------------------------------

LOKA_WORDMARK = """<symbol id="loka-wordmark" viewBox="0 0 93.054802 32.0476">
<path d="M 0,5.61719 H 4.37561 V 22.5767 h 9.04289 v 4.3861 H 0 Z" fill="currentColor"/>
<path d="m 51.9241,5.61719 h 4.6673 V 16.7286 L 68.0263,5.61719 h 5.7758 L 63.534,15.8221 63.2715,16.056 70.885,23.6878 88.9125,5.61719 h 4.1423 V 26.6704 H 88.6792 V 11.7577 L 74.0355,26.6704 H 67.968 l -7.2344,-7.3394 -0.35,-0.3217 -3.7922,3.7136 v 4.2399 h -4.6673 z" fill="currentColor"/>
<path d="m 32.2342,0 c -8.8388,0 -15.9856,7.16392 -15.9856,16.0238 0,8.8599 7.1468,16.0238 15.9856,16.0238 8.8387,0 15.9855,-7.1932 15.9855,-16.0238 C 48.2197,7.16392 41.0729,0 32.2342,0 Z m -0.1167,27.6323 c -6.4176,0 -11.5808,-5.2048 -11.5808,-11.6085 0,-6.43291 5.1924,-11.60848 11.5808,-11.60848 6.4175,0 11.5807,5.20481 11.5807,11.60848 0,6.4037 -5.1923,11.6085 -11.5807,11.6085 z" fill="currentColor"/>
<path d="m 35.7338,16.0285 c 0,1.9006 -1.546,3.4504 -3.4421,3.4504 -1.8961,0 -3.4422,-1.5498 -3.4422,-3.4504 0,-1.9006 1.5461,-3.4504 3.4422,-3.4504 1.8961,0 3.4421,1.5498 3.4421,3.4504 z" fill="currentColor"/>
</symbol>"""


def _sidebar_nav(sections):
    out = []
    for section in sections:
        items = "".join(
            f'<li><a data-nav="{t["path"]}" href="#/{t["path"]}">'
            f'{html.escape(t["short"])}{_chip(t["abbr"])}</a></li>'
            for t in section["terms"]
        )
        title = html.escape(section["title"])
        out.append(
            f'<li class="nav-group" data-group="{section["slug"]}">'
            f'<div class="nav-head-row">'
            f'<a class="nav-head" data-nav="{section["slug"]}" href="#/{section["slug"]}">'
            f"{title}</a>"
            f'<button class="nav-toggle" type="button" aria-expanded="true" '
            f'aria-controls="nav-{section["slug"]}" aria-label="Toggle {title}"></button>'
            f"</div>"
            f'<ul id="nav-{section["slug"]}">{items}</ul></li>'
        )
    return "".join(out)


def _page(sections, articles, search_index, home_meta, readme_html, authors_html):
    art_rows = "\n".join(
        f"<span>{html.escape(row)}</span>" for row in _read(ASCII_ART).splitlines()
    )
    home = (
        '<article class="term home" data-route="" hidden>'
        '<pre class="ascii-art" role="img" aria-label="Loka wordmark drawn in ASCII">'
        f'{art_rows}</pre></article>'
    )
    contributors = (
        '<article class="term" data-route="contributors" hidden>'
        f'{_crumb("contributors")}<h1>Contributors</h1>'
        f'<div class="prose">{authors_html}</div></article>'
    )
    articles_html = "".join(
        [home, _readme(sections, home_meta["tagline"], readme_html)]
        + [_section_page(s) for s in sections]
        + articles
        + [contributors]
    )
    tokens = {
        "%%TITLE%%": html.escape(home_meta["title"]),
        "%%TAGLINE%%": html.escape(home_meta["tagline"]),
        "%%URL%%": html.escape(SITE_URL),
        "%%OGIMAGE%%": html.escape(SITE_URL + SHARE_IMAGE),
        "%%OGWIDTH%%": str(SHARE_SIZE[0]),
        "%%OGHEIGHT%%": str(SHARE_SIZE[1]),
        "%%WORDMARK%%": LOKA_WORDMARK,
        "%%NAV%%": _sidebar_nav(sections),
        "%%ARTICLES%%": articles_html,
        "%%SEARCH%%": json.dumps(search_index, separators=(",", ":")),
        "%%CSS%%": _read(os.path.join(ROOT, "utils", "style.css")),
        "%%JS%%": _read(os.path.join(ROOT, "utils", "app.js")),
    }
    page = _read(os.path.join(ROOT, "utils", "shell.html"))
    for key, value in tokens.items():
        page = page.replace(key, value)
    leftover = re.findall(r"%%[A-Z]+%%", page)
    if leftover:
        raise BuildError(f"unsubstituted template tokens: {sorted(set(leftover))}")
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=os.path.join(ROOT, "index.html"))
    parser.add_argument("--check", action="store_true",
                        help="validate links, diagrams, and the share image "
                             "(does not write index.html)")
    args = parser.parse_args()
    try:
        build(args.out, check_only=args.check)
    except BuildError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
