# -*- coding: utf-8 -*-
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

from odoo.addons.inteligente_content_matrix.models.text_utils import (
    build_live_corpus,
    extract_meta_corpus,
    hash_text,
    html_to_text,
    normalize_text,
    split_multipart_text,
    text_matches,
)


@tagged("post_install", "-at_install")
class TestVerifyApply(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Website = cls.env["copywriting.website"]
        Page = cls.env["copywriting.page"]
        Section = cls.env["copywriting.section"]
        cls.website = Website.create(
            {
                "name": "Verify Site",
                "code": "verify_site",
                "base_url": "https://example.test",
            }
        )
        cls.page = Page.create(
            {
                "website_id": cls.website.id,
                "name": "Home",
                "url": "/",
                "sequence": 10,
            }
        )
        cls.s_ok = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Hero",
                "anchor_key": "home.hero.h1",
                "sequence": 10,
                "role": "h1",
                "content_current": "OLD HERO",
                "content_final": "NEW HERO LIVE",
                "status": "approved",
                "apply_method": "manual_checklist",
            }
        )
        cls.s_drift = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Body",
                "anchor_key": "home.body",
                "sequence": 20,
                "role": "body",
                "content_current": "BODY CURRENT ON LIVE",
                "content_final": "BODY FINAL NOT LIVE",
                "status": "updated",
                "apply_method": "manual_checklist",
            }
        )
        cls.s_missing = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Ghost",
                "anchor_key": "home.ghost",
                "sequence": 30,
                "role": "other",
                "content_current": "NOWHERE",
                "content_final": "ALSO NOWHERE",
                "status": "approved",
                "apply_method": "manual_checklist",
            }
        )

    def test_text_utils(self):
        self.assertEqual(normalize_text("  a\n\tb  "), "a b")
        self.assertTrue(hash_text("x"))
        html = "<html><script>x</script><body><h1>Hello</h1><p>World</p></body></html>"
        self.assertIn("Hello", html_to_text(html))
        self.assertNotIn("x", html_to_text(html))

    def test_meta_corpus_and_multipart_match(self):
        html = """
        <html><head>
          <title>Home | Demo</title>
          <meta name="description" content="This is the homepage of the website"/>
          <meta property="og:description" content="OG desc unused for exact"/>
        </head><body>
          <h2>ENTERTAINED BY MASTERS</h2>
          <h2>OF ENTERTAINMENT</h2>
          <a>Classic</a><a>BOOK</a>
          <p>SELECTED LANDSCAPES GOOFOOT TOURS ZERO TO 50 PERCENT OF TOUR TIME USED TO HELP THE PARK REGENARATION</p>
        </body></html>
        """
        meta = extract_meta_corpus(html)
        self.assertIn("This is the homepage of the website", meta)
        self.assertIn("Home | Demo", meta)
        # meta not in body-only extract
        body_only = normalize_text(html_to_text(html))
        self.assertNotIn("This is the homepage of the website", body_only)

        corpus_meta, kind = build_live_corpus(
            html, role="meta", anchor_key="home.meta.description"
        )
        self.assertEqual(kind, "meta+body")
        ok, mode = text_matches(
            corpus_meta, "This is the homepage of the website"
        )
        self.assertTrue(ok)
        self.assertEqual(mode, "exact")

        parts = split_multipart_text(
            "ENTERTAINED BY MASTERS / OF ENTERTAINMENT"
        )
        self.assertEqual(len(parts), 2)
        body_corpus, _ = build_live_corpus(html, role="h2")
        ok, mode = text_matches(
            body_corpus, "ENTERTAINED BY MASTERS / OF ENTERTAINMENT"
        )
        self.assertTrue(ok)
        self.assertEqual(mode, "multipart")

        # token coverage for lightly reformatted long body
        ok, mode = text_matches(
            body_corpus,
            "SELECTED LANDSCAPES ZERO TO 50 PERCENT OF TOUR TIME USED TO HELP THE PARK REGENARATION",
        )
        self.assertTrue(ok)
        self.assertIn(mode, ("exact", "tokens", "multipart"))

    def test_verify_meta_and_multipart_sections(self):
        Section = self.env["copywriting.section"]
        meta = Section.create(
            {
                "page_id": self.page.id,
                "name": "Meta description",
                "anchor_key": "home.meta.description",
                "sequence": 5,
                "role": "meta",
                "content_current": "This is the homepage of the website",
                "content_final": "",
                "status": "pending_review",
            }
        )
        masters = Section.create(
            {
                "page_id": self.page.id,
                "name": "Masters H2",
                "anchor_key": "home.block.masters_h2",
                "sequence": 15,
                "role": "h2",
                "content_current": "ENTERTAINED BY MASTERS / OF ENTERTAINMENT",
                "content_final": "Entertained by masters of storytelling",
                "status": "approved",
            }
        )
        live_html = """
        <html><head>
          <meta name="description" content="This is the homepage of the website"/>
        </head><body>
          <h1>NEW HERO LIVE</h1>
          <p>BODY CURRENT ON LIVE</p>
          <h2>ENTERTAINED BY MASTERS</h2>
          <h2>OF ENTERTAINMENT</h2>
          <p>ghost nowhere not here</p>
        </body></html>
        """
        run = self.env["copywriting.verify.run"].create(
            {
                "website_id": self.website.id,
                "page_ids": [(6, 0, self.page.ids)],
                "compare_to": "final_then_current",
            }
        )
        with patch.object(type(run), "_fetch_html", return_value=(200, live_html)):
            run.action_run_verify()
        by_anchor = {l.anchor_key: l for l in run.line_ids if l.section_id}
        self.assertEqual(by_anchor["home.meta.description"].result, "ok")
        self.assertIn("meta", by_anchor["home.meta.description"].note)
        # final not live, current multipart matches → drift
        self.assertEqual(by_anchor["home.block.masters_h2"].result, "drift")
        self.assertIn("multipart", by_anchor["home.block.masters_h2"].note)
        self.assertEqual(by_anchor["home.hero.h1"].result, "ok")
        self.assertEqual(by_anchor["home.ghost"].result, "missing_matrix")

    def test_verify_classifies_ok_drift_missing(self):
        live_html = """
        <html><body>
          <h1>NEW HERO LIVE</h1>
          <p>BODY CURRENT ON LIVE</p>
          <p>unrelated chrome</p>
        </body></html>
        """
        run = self.env["copywriting.verify.run"].create(
            {
                "website_id": self.website.id,
                "page_ids": [(6, 0, self.page.ids)],
                "compare_to": "final_then_current",
            }
        )
        with patch.object(
            type(run),
            "_fetch_html",
            return_value=(200, live_html),
        ):
            run.action_run_verify()
        by_anchor = {l.anchor_key: l.result for l in run.line_ids if l.section_id}
        self.assertEqual(by_anchor["home.hero.h1"], "ok")
        self.assertEqual(by_anchor["home.body"], "drift")
        self.assertEqual(by_anchor["home.ghost"], "missing_matrix")
        self.assertIn(run.state, ("warn", "ok"))
        self.assertTrue(run.log_text)
        self.assertGreaterEqual(run.count_ok, 1)
        self.assertGreaterEqual(run.count_drift, 1)
        self.assertGreaterEqual(run.count_missing, 1)

    def test_apply_checklist_dry_run(self):
        run = self.env["copywriting.apply.run"].create(
            {
                "website_id": self.website.id,
                "page_ids": [(6, 0, self.page.ids)],
                "dry_run": True,
            }
        )
        run.action_build_checklist()
        self.assertTrue(run.checklist_html)
        self.assertIn("NEW HERO LIVE", run.checklist_html)
        self.assertEqual(run.count_checklist, 3)
        self.assertTrue(all(l.status == "todo" for l in run.line_ids))
        self.assertEqual(run.state, "ok")

    def test_apply_execute_requires_manager_confirm(self):
        run = self.env["copywriting.apply.run"].create(
            {
                "website_id": self.website.id,
                "dry_run": False,
                "manager_confirm": False,
            }
        )
        # Ensure current user is manager (admin usually is after install)
        if not self.env.user.has_group("inteligente_content_matrix.group_manager"):
            self.env.user.group_ids = [
                (4, self.env.ref("inteligente_content_matrix.group_manager").id)
            ]
        with self.assertRaises(UserError):
            run.action_run_apply()
        run.manager_confirm = True
        run.action_run_apply()
        self.assertTrue(run.line_ids)
        self.assertTrue(all(l.status == "done" for l in run.line_ids))
