# -*- coding: utf-8 -*-
{
    "name": "Inteligente Content Matrix Studio",
    "version": "19.0.1.7.2",
    "category": "Website",
    "summary": "Content matrix and guided copy review for Odoo CE websites",
    "description": """
Content Matrix Studio (P0–P4 + Discuss bot)
==========================================
- Content matrix: website, page, section, versions, dom_id
- Import/export CSV and JSON; DOM anchor map import
- Seed support for InCity pilot
- Review session state machine (P2)
- Discuss chatter/notify + section kanban + operator guide (P3)
- Verify runs (fetch/hash) + manual apply checklist (P4)
- Discuss Matrix Bot: option buttons, combined section cards,
  Website Edit deep-links (?enable_editor=1#dom_id) with iframe scroll
    """,
    "author": "Inteligente / WeRa Global",
    "license": "LGPL-3",
    "depends": ["mail", "website", "portal"],
    "data": [
        "security/content_matrix_security.xml",
        "security/ir.model.access.csv",
        "data/matrix_bot_data.xml",
        "views/copywriting_website_views.xml",
        "views/copywriting_page_views.xml",
        "views/copywriting_section_views.xml",
        "views/copywriting_session_views.xml",
        "views/copywriting_verify_views.xml",
        "views/copywriting_apply_views.xml",
        "views/wizards.xml",
        "views/menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "inteligente_content_matrix/static/src/discuss/matrix_bot_choices.js",
            "inteligente_content_matrix/static/src/discuss/matrix_bot_choices.scss",
        ],
    },
    "installable": True,
    "application": True,
}
