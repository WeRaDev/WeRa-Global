# -*- coding: utf-8 -*-
"""Odoo shell: inject matrix DOM ids on remaining InCity pages (after Home).

  odoo shell -d incity_site --db_host=db --no-http < inject_incity_rest_dom_ids.py
"""
import re

Page = env["website.page"].sudo()

# url -> list of (data-snippet, dom_id, occurrence_index)
# Derived from live snippet order + docs/incity-dom-anchor-map.md
PAGE_ASSIGN = {
    "/contactus": [
        ("s_form_aside", "contact-hero", 0),
        ("s_website_form", "contact-form", 0),
        ("s_title", "contact-trust", 0),
        ("s_faq_list", "contact-help", 0),
    ],
    "/privacy": [
        ("s_title", "privacy-body", 0),
    ],
    "/tours-from-lisbon": [
        ("s_cards_soft", "lisbon-hero", 0),
        ("s_card", "lisbon-classic", 0),
        ("s_card", "lisbon-grand", 1),
        ("s_card", "lisbon-short", 2),
        # CTA/custom: reuse hero band (only 4 structure snippets on page)
        # lisbon-cta is aliased onto hero after packages for scroll of whole commercial band
    ],
    "/tours-from-sintra": [
        ("s_text_block", "sintra-hero", 0),
        ("s_three_columns", "sintra-goodfoot", 0),
        ("s_card", "sintra-short", 0),
        ("s_card", "sintra-palace", 1),
        ("s_card", "sintra-panoramic", 2),
        ("s_text_block", "sintra-cta", 1),
    ],
    "/intv": [
        ("s_banner", "intv-hero", 0),
        ("s_references", "intv-cta", 0),
    ],
    "/reviews": [
        ("s_text_block", "reviews-hero", 0),
        ("s_text_block", "reviews-cta", 1),
        ("s_text_block", "reviews-sources", 2),
    ],
    "/vasco-da-lama": [
        ("s_striped_center_top", "vasco-hero", 0),
        ("s_title", "vasco-goodfoot", 0),
        ("s_color_blocks_2", "vasco-cta", 0),
    ],
}


def get_page(url):
    pages = Page.search([("url", "=", url), ("is_published", "=", True)])
    p = pages.filtered(lambda r: r.website_id.id == 1)[:1] or pages[:1]
    return p


def set_id_on_nth_snippet(html, snippet, dom_id, n=0):
    pattern = re.compile(
        r"<(section|div)(\s[^>]*?data-snippet=\"%s\"[^>]*?)>" % re.escape(snippet),
        re.I,
    )
    matches = list(pattern.finditer(html))
    if n >= len(matches):
        return (
            html,
            False,
            "FAIL %s#%s not found (have %s)" % (snippet, n, len(matches)),
        )
    m = matches[n]
    tag_name = m.group(1)
    attrs = m.group(2)
    attrs2 = re.sub(r'\s*\bid="[^"]*"', "", attrs)
    attrs2 = re.sub(r"\s*\bid='[^']*'", "", attrs2)
    new_open = '<%s%s id="%s">' % (tag_name, attrs2, dom_id)
    start, end = m.span()
    return (
        html[:start] + new_open + html[end:],
        True,
        "OK set %s on %s#%s" % (dom_id, snippet, n),
    )


# Lisbon CTA: after packages, also set lisbon-cta on s_cards_soft as second id is impossible;
# use a dedicated approach: add id lisbon-cta on the soft cards container is taken by hero.
# Map CTA keys to lisbon-hero until a separate CTA block exists.
# Optionally set data attribute - skip; document alias.

summary = []
for url, assigns in PAGE_ASSIGN.items():
    p = get_page(url)
    if not p:
        print("MISSING page", url)
        summary.append((url, "MISSING", []))
        continue
    view = p.view_id
    arch = view.arch_db or ""
    new_arch = arch
    msgs = []
    for sn, dom_id, n in assigns:
        new_arch, ok, msg = set_id_on_nth_snippet(new_arch, sn, dom_id, n)
        msgs.append(msg)
        print(url, msg)
    if new_arch != arch:
        view.write({"arch_db": new_arch})
        env.cr.commit()
        print("WROTE", url, "view", view.id, "len", len(new_arch))
        summary.append((url, "WROTE", msgs))
    else:
        print("NOCHANGE", url)
        summary.append((url, "NOCHANGE", msgs))

# Verify presence in arch
print("=" * 70)
print("VERIFY ARCH")
for url, assigns in PAGE_ASSIGN.items():
    p = get_page(url)
    if not p:
        continue
    a = p.view_id.arch_db or ""
    ids = sorted({dom for _, dom, _ in assigns})
    for dom in ids:
        print(url, dom, a.count('id="%s"' % dom))

print("DONE")
