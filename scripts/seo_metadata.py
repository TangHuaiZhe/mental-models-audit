"""Generate page-specific search descriptions without changing course sources."""

from html import unescape
import re


DEFINITION_HEADING = re.compile(r"^##(?:\s+\d+\.)?\s*一句话定义\s*$")
MARKDOWN_LINK = re.compile(r"!?\[([^]]*)\]\([^)]*\)")
HTML_TAG = re.compile(r"<[^>]+>")
INLINE_MARKUP = re.compile(r"[*_`~]+")
LEADING_MARKER = re.compile(r"^(?:>\s*|[-+*]\s+|\d+[.)]\s+)+")
WHITESPACE = re.compile(r"\s+")
SENTENCE_END = re.compile(r"[。！？；]")


def _plain_text(value):
    value = MARKDOWN_LINK.sub(r"\1", value)
    value = HTML_TAG.sub(" ", value)
    value = INLINE_MARKUP.sub("", value)
    value = LEADING_MARKER.sub("", value.strip())
    return WHITESPACE.sub(" ", unescape(value)).strip()


def _truncate(value, limit):
    if len(value) <= limit:
        return value
    candidate = value[: limit + 1]
    endings = [match.end() for match in SENTENCE_END.finditer(candidate)]
    if endings and endings[-1] >= limit // 2:
        return candidate[: endings[-1]].strip()
    return value[:limit].rstrip(" ，、：；") + "…"


def extract_course_description(markdown, limit=160):
    """Return plain text from a lesson's one-sentence-definition section."""
    lines = markdown.splitlines()
    start = next(
        (index + 1 for index, line in enumerate(lines) if DEFINITION_HEADING.match(line)),
        None,
    )
    if start is None:
        return None

    fragments = []
    in_math_block = False
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("##"):
            break
        if stripped == "$$":
            in_math_block = not in_math_block
            continue
        if in_math_block or not stripped:
            continue
        fragment = _plain_text(stripped)
        if fragment:
            fragments.append(fragment)

    if not fragments:
        return None
    return _truncate(" ".join(fragments), limit)


def on_page_markdown(markdown, page, config, files):
    """Set Material for MkDocs metadata for course pages at build time."""
    source_uri = getattr(getattr(page, "file", None), "src_uri", "")
    if (
        source_uri.startswith("course/")
        and source_uri.endswith(".md")
        and not page.meta.get("description")
    ):
        description = extract_course_description(markdown)
        if description:
            page.meta["description"] = description
    return markdown
