"""A small Markdown subset renderer.

Deliberately narrow: it supports exactly the constructs the glossary uses, so the
build stays dependency-free. Unsupported syntax is passed through as text rather
than silently mangled.
"""

import html
import re

__all__ = ["render_markdown", "strip_markdown", "parse_frontmatter"]

_FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n?", re.S)


def parse_frontmatter(text):
    """Split a leading YAML-ish frontmatter block from the body.

    Only flat `key: value` pairs are supported, which is all the glossary needs.

    Args:
        text: Full file contents.

    Returns:
        A `(meta, body)` tuple where `meta` maps string keys to string values.
    """
    match = _FRONTMATTER.match(text)
    if not match:
        return {}, text
    meta = {}
    for line in match.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        meta[key.strip()] = value
    return meta, text[match.end():]


# --- inline -----------------------------------------------------------------

_CODE_SPAN = re.compile(r"`([^`]+)`")
_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
_UNDERSCORE_ITALIC = re.compile(r"(?<![\w_])_([^_\n]+)_(?![\w_])")


def _inline_pass(text, link_resolver, slots):
    """Render inline markup, stashing finished HTML in `slots` as placeholders."""

    def stash(markup):
        slots.append(markup)
        return f"\x00{len(slots) - 1}\x00"

    text = _CODE_SPAN.sub(
        lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), text
    )

    # Stash images before links so the leading "!" is not left stranded.
    text = _IMAGE.sub(
        lambda m: stash(
            f'<img src="{html.escape(m.group(2))}" alt="{html.escape(m.group(1))}">'
        ),
        text,
    )

    def on_link(match):
        label, href = match.group(1), match.group(2)
        resolved, external = link_resolver(href)
        attrs = ' target="_blank" rel="noopener"' if external else ""
        cls = ' class="ext"' if external else ""
        inner = _inline_pass(label, link_resolver, slots)
        return stash(f'<a href="{html.escape(resolved)}"{cls}{attrs}>{inner}</a>')

    text = _LINK.sub(on_link, text)

    text = html.escape(text)
    text = _BOLD.sub(r"<strong>\1</strong>", text)
    text = _ITALIC.sub(r"<em>\1</em>", text)
    text = _UNDERSCORE_ITALIC.sub(r"<em>\1</em>", text)
    return text


_PLACEHOLDER = re.compile(r"\x00(\d+)\x00")


def _render_inline(text, link_resolver):
    """Render inline markdown to HTML, protecting code spans from formatting."""
    slots = []
    text = _inline_pass(text, link_resolver, slots)
    # Placeholders can nest (a link label containing code), so expand to a fixed point.
    for _ in range(12):
        expanded = _PLACEHOLDER.sub(lambda m: slots[int(m.group(1))], text)
        if expanded == text:
            break
        text = expanded
    return text


# --- blocks -----------------------------------------------------------------

_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_ULI = re.compile(r"^(\s*)[-*]\s+(.*)$")
_OLI = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
_TABLE_SEP = re.compile(r"^\s*\|?[\s:-]*-[\s:|-]*\|?\s*$")


def _slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", text)


def render_markdown(text, link_resolver=None, image_resolver=None, heading_offset=1):
    """Render a Markdown subset to an HTML string.

    Args:
        text: Markdown body (frontmatter already stripped).
        link_resolver: Callable mapping an href to `(resolved_href, is_external)`.
        image_resolver: Callable mapping `(alt, src)` to an HTML string.
        heading_offset: Added to each heading level, so `#` becomes `<h2>` by default.

    Returns:
        Rendered HTML.
    """
    if link_resolver is None:
        link_resolver = lambda href: (href, href.startswith(("http://", "https://")))
    if image_resolver is None:
        image_resolver = lambda alt, src: (
            f'<img src="{html.escape(src)}" alt="{html.escape(alt)}">'
        )

    lines = text.split("\n")
    out = []
    i = 0
    n = len(lines)

    def inline(s):
        return _render_inline(s, link_resolver)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            code = html.escape("\n".join(buf))
            out.append(f"<pre><code{cls}>{code}</code></pre>")
            continue

        # horizontal rule
        if re.fullmatch(r"(\*\s*){3,}|(-\s*){3,}|(_\s*){3,}", stripped):
            out.append("<hr>")
            i += 1
            continue

        # heading
        m = _HEADING.match(stripped)
        if m:
            level = min(len(m.group(1)) + heading_offset, 6)
            content = inline(m.group(2).strip())
            anchor = _slugify(m.group(2))
            out.append(
                f'<h{level} id="{anchor}">{content}'
                f'<a class="heading-anchor" href="#{anchor}" aria-label="Link to this section">#</a>'
                f"</h{level}>"
            )
            i += 1
            continue

        # blockquote
        if stripped.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = render_markdown(
                "\n".join(buf), link_resolver, image_resolver, heading_offset
            )
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # standalone image (figure)
        m = _IMAGE.fullmatch(stripped)
        if m:
            out.append(image_resolver(m.group(1), m.group(2)))
            i += 1
            continue

        # table
        if stripped.startswith("|") and i + 1 < n and _TABLE_SEP.match(lines[i + 1]):
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head = "".join(f"<th>{inline(c)}</th>" for c in header)
            body = "".join(
                "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(
                f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead>'
                f"<tbody>{body}</tbody></table></div>"
            )
            continue

        # lists
        m_u, m_o = _ULI.match(line), _OLI.match(line)
        if m_u or m_o:
            ordered = bool(m_o)
            i, markup = _render_list(lines, i, ordered, inline)
            out.append(markup)
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not _is_block_start(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")
        else:
            i += 1

    return "\n".join(out)


def _is_block_start(line):
    s = line.strip()
    return bool(
        s.startswith(("```", ">", "|"))
        or _HEADING.match(s)
        or _ULI.match(line)
        or _OLI.match(line)
        or re.fullmatch(r"(\*\s*){3,}|(-\s*){3,}", s)
    )


def _render_list(lines, i, ordered, inline):
    """Render one list, recursing into indented sub-lists."""
    tag = "ol" if ordered else "ul"
    base_indent = len(lines[i]) - len(lines[i].lstrip())
    items = []
    n = len(lines)

    while i < n:
        line = lines[i]
        if not line.strip():
            # a blank line ends the list unless the next line continues it
            if i + 1 < n and (_ULI.match(lines[i + 1]) or _OLI.match(lines[i + 1])):
                nxt = lines[i + 1]
                if len(nxt) - len(nxt.lstrip()) >= base_indent:
                    i += 1
                    continue
            break
        m_o = _OLI.match(line)
        m = m_o or _ULI.match(line)
        if not m:
            break
        indent = len(m.group(1))
        if indent < base_indent:
            break
        if indent == base_indent and bool(m_o) != ordered:
            break
        if indent > base_indent:
            sub_ordered = bool(_OLI.match(line))
            i, sub = _render_list(lines, i, sub_ordered, inline)
            if items and items[-1].endswith("</li>"):
                items[-1] = items[-1][: -len("</li>")] + sub + "</li>"
            else:
                items.append(sub)
            continue
        content = m.group(2).strip()
        i += 1
        # fold continuation lines into the item
        cont = []
        while i < n and lines[i].strip() and not (_ULI.match(lines[i]) or _OLI.match(lines[i])):
            ind = len(lines[i]) - len(lines[i].lstrip())
            if ind <= base_indent and _is_block_start(lines[i]):
                break
            if ind <= base_indent:
                break
            cont.append(lines[i].strip())
            i += 1
        if cont:
            content += " " + " ".join(cont)
        items.append(f"<li>{inline(content)}</li>")

    body = "".join(items)
    return i, f"<{tag}>{body}</{tag}>"


_MD_STRIP = [
    (re.compile(r"```.*?```", re.S), " "),
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), " "),
    (re.compile(r"\[([^\]]+)\]\([^)]*\)"), r"\1"),
    (re.compile(r"[#*`>|_]"), " "),
]


def strip_markdown(text):
    """Reduce markdown to plain text, for the search index."""
    for pattern, repl in _MD_STRIP:
        text = pattern.sub(repl, text)
    return re.sub(r"\s+", " ", text).strip()
