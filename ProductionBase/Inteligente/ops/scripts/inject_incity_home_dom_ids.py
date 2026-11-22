# -*- coding: utf-8 -*-
"""Odoo shell script: inject matrix DOM ids on InCity homepage (+ footer).

Run inside container:
  odoo shell -d incity_site --db_host=db --no-http < inject_incity_home_dom_ids.py
"""
import re

Page = env["website.page"].sudo()
View = env["ir.ui.view"].sudo()

homes = Page.search([("url", "=", "/")])
p = homes.filtered(lambda r: "EASY SINTRA" in (r.view_id.arch_db or ""))[:1]
assert p, "home page with content not found"
view = p.view_id
arch = view.arch_db or ""
print("BEFORE page", p.id, "view", view.id, "len", len(arch))

# (data-snippet, dom_id, occurrence_index) — live Home order
ASSIGN = [
    ("s_striped_center_top", "home-hero", 0),
    ("s_title", "home-masters", 0),
    ("s_color_blocks_2", "home-tours", 0),
    ("s_image_hexagonal", "home-goodfoot", 0),
    ("s_image_punchy", "home-harmony", 0),
    ("s_masonry_block", "home-bio", 0),
    ("s_masonry_block_default_template", "home-regenerative", 0),
    ("s_masonry_block", "home-experiences", 1),
    ("s_quadrant", "home-book-band", 0),
    ("s_popup", "home-promo-popup", 0),
]


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
            "snippet %s occurrence %s not found (have %s)"
            % (snippet, n, len(matches)),
        )
    m = matches[n]
    tag_name = m.group(1)
    attrs = m.group(2)
    attrs2 = re.sub(r'\s*\bid="[^"]*"', "", attrs)
    attrs2 = re.sub(r"\s*\bid='[^']*'", "", attrs2)
    new_open = '<%s%s id="%s">' % (tag_name, attrs2, dom_id)
    start, end = m.span()
    return html[:start] + new_open + html[end:], True, "set %s on %s#%s" % (
        dom_id,
        snippet,
        n,
    )


new_arch = arch
for sn, dom_id, n in ASSIGN:
    new_arch, ok, msg = set_id_on_nth_snippet(new_arch, sn, dom_id, n)
    print(("OK" if ok else "FAIL"), msg)

if new_arch != arch:
    view.write({"arch_db": new_arch})
    env.cr.commit()
    print("WROTE homepage view", view.id, "new_len", len(new_arch))
else:
    print("NOCHANGE homepage")

# Footer: first section inside #footer gets id=global-footer
found_footer = View.browse()
for v in View.search(
    [("type", "=", "qweb"), ("website_id", "in", [False, p.website_id.id])]
):
    a = v.arch_db or ""
    if 'id="footer"' in a or "id='footer'" in a:
        found_footer |= v
print("views with id=footer", [(v.id, v.key, v.name) for v in found_footer])

target = View.browse()
for v in found_footer:
    if v.website_id and v.website_id.id == p.website_id.id:
        target = v
        break
if not target:
    for v in found_footer:
        a = v.arch_db or ""
        if "oe_structure" in a:
            target = v
            break
if not target and found_footer:
    target = found_footer.sorted("id", reverse=True)[:1]

if target:
    fa = target.arch_db or ""
    print("FOOTER target", target.id, target.key, "len", len(fa))
    if 'id="global-footer"' in fa:
        print("global-footer already present")
    else:
        m = re.search(r'(<div[^>]*id="footer"[^>]*>)', fa)
        if not m:
            print("NO id=footer open tag in target")
        else:
            pos = m.end()
            rest = fa[pos:]
            sm = re.search(r"<(section)(\s[^>]*?)?>", rest)
            if sm:
                attrs = sm.group(2) or ""
                attrs2 = re.sub(r'\s*\bid="[^"]*"', "", attrs)
                attrs2 = re.sub(r"\s*\bid='[^']*'", "", attrs2)
                new_sec = '<section%s id="global-footer">' % attrs2
                fa2 = fa[:pos] + rest[: sm.start()] + new_sec + rest[sm.end() :]
                target.write({"arch_db": fa2})
                env.cr.commit()
                print("WROTE global-footer on first section in footer view", target.id)
            else:
                print("NO section inside #footer")
else:
    print("NO footer view found to edit")

arch2 = view.arch_db or ""
for dom in [
    "home-hero",
    "home-masters",
    "home-tours",
    "home-goodfoot",
    "home-harmony",
    "home-bio",
    "home-regenerative",
    "home-experiences",
    "home-book-band",
    "home-promo-popup",
]:
    print("HAS", dom, arch2.count('id="%s"' % dom))
