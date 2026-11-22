# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCopywritingSessionFlow(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Website = cls.env["copywriting.website"]
        Page = cls.env["copywriting.page"]
        Section = cls.env["copywriting.section"]
        cls.website = Website.create(
            {
                "name": "Test Site",
                "code": "test_matrix",
                "executive_summary": "<p>Summary</p>",
            }
        )
        cls.page = Page.create(
            {
                "website_id": cls.website.id,
                "name": "Home",
                "url": "/",
                "sequence": 10,
                "analysis_html": "<p>Analysis</p>",
                "guidelines_html": "<p>Guidelines</p>",
            }
        )
        cls.s1 = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Hero",
                "anchor_key": "home.hero.h1",
                "sequence": 10,
                "role": "h1",
                "content_current": "OLD",
                "content_interpretation": "Means X",
                "content_suggestion": "NEW TITLE",
                "status": "pending_review",
            }
        )
        cls.s2 = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Body",
                "anchor_key": "home.hero.body",
                "sequence": 20,
                "role": "body",
                "content_current": "BODY OLD",
                "content_interpretation": "Means Y",
                "content_suggestion": "BODY NEW",
                "status": "pending_review",
            }
        )

    def test_happy_path_accept_both(self):
        Session = self.env["copywriting.session"]
        session = Session.create({"website_id": self.website.id})
        session.action_start()
        self.assertEqual(session.state, "intro")
        session.action_proceed()
        self.assertEqual(session.state, "page_select")
        session.current_page_id = self.page
        session.action_choose_page()
        self.assertEqual(session.state, "page_intro")
        session.action_start_sections()
        self.assertEqual(session.state, "section_fact")
        self.assertEqual(session.current_section_id, self.s1)
        session.action_next_step()
        self.assertEqual(session.state, "section_interpret")
        session.action_next_step()
        self.assertEqual(session.state, "section_suggest")
        session.action_next_step()
        self.assertEqual(session.state, "section_decide")
        session.action_accept_suggestion()
        self.assertEqual(self.s1.status, "approved")
        self.assertEqual(self.s1.content_final, "NEW TITLE")
        self.assertEqual(session.current_section_id, self.s2)
        self.assertEqual(session.state, "section_fact")
        # finish second via edit
        session.action_next_step()
        session.action_next_step()
        session.action_next_step()
        session.action_enable_edit_mode()
        self.s2.content_final = "BODY EDITED"
        session.action_save_edit()
        self.assertEqual(self.s2.status, "updated")
        self.assertEqual(self.s2.content_final, "BODY EDITED")
        self.assertEqual(session.state, "page_done")
        self.assertEqual(self.page.status, "done")
        session.action_finish()
        self.assertEqual(session.state, "finished")
        self.assertTrue(session.event_ids)
        # Discuss: finish posts a message on the thread
        self.assertTrue(session.message_ids)
        bodies = " ".join((session.message_ids.mapped("body") or []))
        self.assertIn("finished", bodies.lower())
        # operator should be subscribed when partner is available
        partner = session.user_id.partner_id
        if partner:
            followers = session.message_follower_ids.mapped("partner_id")
            self.assertIn(partner, followers)

    def test_pause_resume_and_notify(self):
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        session.action_start()
        session.action_later()
        self.assertEqual(session.state, "paused")
        self.assertEqual(session.resume_state, "intro")
        session.action_resume()
        self.assertEqual(session.state, "intro")
        self.assertFalse(session.resume_state)

    def test_reject_requires_note(self):
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        session.action_start()
        session.action_proceed()
        session.current_page_id = self.page
        session.action_choose_page()
        session.action_start_sections()
        session.action_next_step()
        session.action_next_step()
        session.action_next_step()
        with self.assertRaises(UserError):
            session.action_reject_interpretation()
        session.reject_note = "Wrong audience"
        session.action_reject_interpretation()
        self.assertEqual(session.state, "section_interpret")
        self.assertEqual(self.s1.status, "rejected_interp")

    def test_illegal_transition(self):
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        with self.assertRaises(UserError):
            session.action_proceed()

    def test_one_active_session(self):
        Session = self.env["copywriting.session"]
        s1 = Session.create({"website_id": self.website.id})
        s1.action_start()
        with self.assertRaises(ValidationError):
            Session.create({"website_id": self.website.id})
