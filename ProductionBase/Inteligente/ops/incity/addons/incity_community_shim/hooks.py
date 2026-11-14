"""Post-install/update repairs for SaaS dump on community Odoo 19."""

import logging
import re

_logger = logging.getLogger(__name__)

_SNIPPET_KEYS = (
    "website.snippets",
    "website.external_snippets",
    "website.snippet_options",
    "website.snippets_menu",
    "website.show_snippet_menu",
)


def ensure_snippet_view_groups(env):
    group_user = env.ref("base.group_user", raise_if_not_found=False)
    if not group_user:
        _logger.warning("base.group_user missing; skip snippet group repair")
        return
    views = env["ir.ui.view"].sudo().search(
        [
            "|",
            ("key", "in", list(_SNIPPET_KEYS)),
            "|",
            ("key", "=like", "website.s\\_%"),
            ("key", "=like", "%.snippets"),
        ]
    )
    fixed = 0
    for view in views:
        if group_user not in view.group_ids:
            view.write({"group_ids": [(4, group_user.id)]})
            fixed += 1
    if fixed:
        _logger.info("incity_community_shim: attached base.group_user on %s snippet views", fixed)


def ensure_offline_template_icon(env):
    """SaaS dump arch calls odoo_icon.to_base64(); community controller already
    passes base64 str/bytes. Align DB arch with filesystem template.
    """
    views = env["ir.ui.view"].sudo().search([("key", "=", "web.webclient_offline")])
    for view in views:
        # arch_db may be dict (translated) or str depending on version
        arch = view.arch_db
        changed = False
        if isinstance(arch, dict):
            new = {}
            for lang, xml in arch.items():
                if xml and "to_base64()" in xml:
                    new[lang] = xml.replace("odoo_icon.to_base64()", "odoo_icon").replace(
                        "{{odoo_icon.to_base64()}}", "{{odoo_icon}}"
                    )
                    changed = True
                else:
                    new[lang] = xml
            if changed:
                view.write({"arch_db": new})
        elif isinstance(arch, str) and "to_base64()" in arch:
            view.write(
                {
                    "arch_db": arch.replace("odoo_icon.to_base64()", "odoo_icon").replace(
                        "{{odoo_icon.to_base64()}}", "{{odoo_icon}}"
                    )
                }
            )
            changed = True
        # also via arch field if needed
        try:
            a = view.arch
            if isinstance(a, str) and "to_base64()" in a:
                view.write({"arch": a.replace("odoo_icon.to_base64()", "odoo_icon")})
                changed = True
        except Exception:
            pass
        if changed:
            _logger.info("incity_community_shim: fixed web.webclient_offline icon base64 call (view %s)", view.id)


def post_init_hook(env):
    ensure_snippet_view_groups(env)
    ensure_offline_template_icon(env)
