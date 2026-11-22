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




def ensure_auth_signup_users_form_safe(env):
    """SaaS arch references widget auth_signup.button_reset_password_link which
    is not registered on Community assets → Owl KeyNotFoundError on Users form.

    Keep the plain action_reset_password buttons; drop only the missing widget.
    """
    View = env["ir.ui.view"].sudo().with_context(active_test=False)
    data = (
        env["ir.model.data"]
        .sudo()
        .search(
            [
                ("module", "=", "auth_signup"),
                ("name", "=", "res_users_view_form"),
                ("model", "=", "ir.ui.view"),
            ],
            limit=1,
        )
    )
    views = View.browse(data.res_id) if data else View.browse()
    if not views:
        views = View.search(
            [
                ("name", "=", "res.users.form.inherit"),
                ("model", "=", "res.users"),
            ]
        )
    needle = 'widget name="auth_signup.button_reset_password_link"'
    fixed = 0
    for view in views:
        arch = view.arch_db
        if not arch:
            continue

        def _scrub(xml):
            if not xml or needle not in xml:
                return xml, False
            # Remove the whole widget node (self-closing or with attrs).
            new_xml = re.sub(
                r"\s*<widget\b[^>]*name=[\"']auth_signup\.button_reset_password_link[\"'][^>]*/>",
                "",
                xml,
            )
            return new_xml, new_xml != xml

        changed = False
        if isinstance(arch, dict):
            new_arch = {}
            for lang, xml in arch.items():
                scrubbed, did = _scrub(xml)
                new_arch[lang] = scrubbed
                changed = changed or did
            if changed:
                view.write({"arch_db": new_arch})
                fixed += 1
        elif isinstance(arch, str):
            scrubbed, did = _scrub(arch)
            if did:
                view.write({"arch_db": scrubbed})
                fixed += 1
    if fixed:
        _logger.info(
            "incity_community_shim: removed SaaS reset-password widget from %s users form view(s)",
            fixed,
        )


def ensure_apps_module_views_safe(env):
    """SaaS dump may leave Apps form inherits pointing at enterprise fields.

    Prefer model stubs (ir_module_module.py). Also deactivate known-bad inherits
    so combined arches stay loadable even before upgrade.
    """
    View = env["ir.ui.view"].sudo().with_context(active_test=False)
    # Known bad inherit from base_import_module Apps form
    data = env["ir.model.data"].sudo().search(
        [
            ("module", "=", "base_import_module"),
            ("name", "=", "module_form_apps_inherit"),
            ("model", "=", "ir.ui.view"),
        ],
        limit=1,
    )
    if data:
        view = View.browse(data.res_id)
        if view.exists() and view.active:
            # Keep active if stubs present; only force-off if field still missing
            if "total_lines_of_code" not in env["ir.module.module"]._fields:
                env.cr.execute(
                    "UPDATE ir_ui_view SET active=false WHERE id=%s", (view.id,)
                )
                _logger.info(
                    "incity_community_shim: deactivated Apps form inherit view %s",
                    view.id,
                )

def post_init_hook(env):
    ensure_snippet_view_groups(env)
    ensure_offline_template_icon(env)
    ensure_apps_module_views_safe(env)
    ensure_auth_signup_users_form_safe(env)
