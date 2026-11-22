# -*- coding: utf-8 -*-
import hashlib
import re
import unicodedata
from html.parser import HTMLParser


def normalize_text(text):
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    return " ".join(text.split())


def hash_text(text):
    norm = normalize_text(text)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest() if norm else ""


class _HTMLTextExtractor(HTMLParser):
    """Strip tags/scripts/styles; keep visible text."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._chunks = []
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg", "template"):
            self._skip_depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg", "template") and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data):
        if self._skip_depth:
            return
        if data and data.strip():
            self._chunks.append(data)

    def text(self):
        return " ".join(self._chunks)


def html_to_text(html):
    if not html:
        return ""
    cleaned = re.sub(
        r"(?is)<(script|style|noscript|svg|template)\b.*?</\1>",
        " ",
        html,
    )
    parser = _HTMLTextExtractor()
    try:
        parser.feed(cleaned)
        parser.close()
    except Exception:
        return re.sub(r"(?s)<[^>]+>", " ", cleaned)
    return parser.text()


_ATTR_RE = re.compile(
    r"""([^\s=]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s>]+))""",
    re.I,
)


def _attr_map(attr_string):
    """Parse HTML attribute blob into lower-case name -> value."""
    attrs = {}
    for name, v1, v2, v3 in _ATTR_RE.findall(attr_string or ""):
        attrs[name.lower()] = v1 or v2 or v3 or ""
    return attrs


_META_NAMES = frozenset(
    (
        "description",
        "og:description",
        "twitter:description",
        "og:title",
        "twitter:title",
        "title",
    )
)


def extract_meta_corpus(html):
    """
    Build a normalized searchable corpus from document head metadata.

    Includes: <title>, meta name=description, og:/twitter: title & description.
    """
    if not html:
        return ""
    parts = []

    for m in re.finditer(r"(?is)<title[^>]*>(.*?)</title>", html):
        parts.append(re.sub(r"(?s)<[^>]+>", " ", m.group(1)))

    for m in re.finditer(r"(?is)<meta\b([^>]*)/?>", html):
        attrs = _attr_map(m.group(1))
        name = (
            attrs.get("name")
            or attrs.get("property")
            or attrs.get("itemprop")
            or ""
        ).lower()
        content = attrs.get("content") or ""
        if content and name in _META_NAMES:
            parts.append(content)

    return normalize_text(" ".join(parts))


# Separators that often join multi-node UI copy in matrix seeds
_PART_SPLIT_RE = re.compile(
    r"(?:"
    r"\s*/\s*"
    r"|\s*·\s*"
    r"|\s*•\s*"
    r"|\s*\|\s*"
    r"|\s*[—–]\s*"
    r"|\r?\n+"
    r"|\s{2,}"
    r")"
)

_MIN_PART_LEN = 3
_MIN_TOKEN_LEN = 4
_TOKEN_COVERAGE = 0.75


def split_multipart_text(text):
    """Split matrix text into normalized parts for multi-node matching."""
    if not text:
        return []
    raw = unicodedata.normalize("NFKC", text or "")
    chunks = _PART_SPLIT_RE.split(raw)
    parts = []
    seen = set()
    for chunk in chunks:
        n = normalize_text(chunk)
        if len(n) < _MIN_PART_LEN:
            continue
        key = n.lower()
        if key in seen:
            continue
        seen.add(key)
        parts.append(n)
    if not parts:
        n = normalize_text(text)
        return [n] if n else []
    return parts


def significant_tokens(text_norm):
    """Alphanumeric tokens long enough for coverage matching."""
    if not text_norm:
        return []
    tokens = re.findall(
        r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]{%d,}" % _MIN_TOKEN_LEN,
        text_norm,
    )
    out, seen = [], set()
    for t in tokens:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def text_contains(haystack_norm, needle_norm):
    """True if needle appears in haystack (both already normalized)."""
    if not needle_norm or not haystack_norm:
        return False
    return needle_norm in haystack_norm


def text_matches(haystack_norm, needle_text, multipart=True):
    """
    Match matrix needle against a normalized haystack.

    Returns (matched, mode) where mode is: exact | multipart | tokens | none
    """
    if not haystack_norm:
        return False, "none"
    needle_norm = normalize_text(needle_text)
    if not needle_norm:
        return False, "none"

    if text_contains(haystack_norm, needle_norm):
        return True, "exact"

    if not multipart:
        return False, "none"

    parts = split_multipart_text(needle_text)
    if len(parts) >= 2 and all(text_contains(haystack_norm, p) for p in parts):
        return True, "multipart"

    tokens = significant_tokens(needle_norm)
    if len(tokens) >= 3:
        hay_l = haystack_norm.lower()
        hits = sum(1 for t in tokens if t.lower() in hay_l)
        if hits / float(len(tokens)) >= _TOKEN_COVERAGE:
            return True, "tokens"

    return False, "none"


def build_live_corpus(html, role=None, anchor_key=None):
    """
    Build the haystack used for a section.

    - role 'meta' or anchor containing '.meta.' → meta corpus (+ body backup)
    - otherwise → visible body (+ meta backup)
    """
    body = normalize_text(html_to_text(html))
    meta = extract_meta_corpus(html)
    role = (role or "").lower()
    anchor = (anchor_key or "").lower()
    is_meta = role == "meta" or ".meta." in anchor or anchor.endswith(".meta")
    if is_meta:
        return normalize_text(" ".join(x for x in (meta, body) if x)), "meta+body"
    if meta:
        return normalize_text(body + " " + meta), "body+meta"
    return body, "body"
