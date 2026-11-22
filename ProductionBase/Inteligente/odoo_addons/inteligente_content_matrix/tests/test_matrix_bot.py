# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestMatrixBotAndPreview(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Website = cls.env["copywriting.website"]
        Page = cls.env["copywriting.page"]
        Section = cls.env["copywriting.section"]
        cls.website = Website.create(
            {
                "name": "Bot Site",
                "code": "botsite",
                "base_url": "https://example.test",
                "executive_summary": "<p>Sum</p>",
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
        cls.section = Section.create(
            {
                "page_id": cls.page.id,
                "name": "Hero",
                "anchor_key": "home.hero.h1",
                "dom_id": "home-hero",
                "sequence": 10,
                "role": "h1",
                "content_current": "OLD",
                "content_interpretation": "X",
                "content_suggestion": "NEW",
                "status": "pending_review",
            }
        )
        # grant operator group to admin user used in tests
        group = cls.env.ref("inteligente_content_matrix.group_operator")
        cls.env.user.write({"group_ids": [(4, group.id)]})

    def test_section_preview_url(self):
        url = self.section.get_preview_url()
        self.assertEqual(url, "https://example.test/#home-hero")

    def test_session_step_card_includes_preview(self):
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        session.action_start()
        session.action_proceed()
        session.current_page_id = self.page
        session.action_choose_page()
        session.action_start_sections()
        html = session._format_step_card_html(include_preview=True)
        self.assertIn("home-hero", html)
        self.assertIn("Open in editor", html)
        self.assertIn("enable_editor=1", html)

    def test_bot_help_and_start_status(self):
        bot_partner = self.env.ref("inteligente_content_matrix.partner_matrix_bot")
        Channel = self.env["discuss.channel"]
        user_partner = self.env.user.partner_id
        # Odoo 19 private chat with bot (current user added automatically)
        channel = Channel._get_or_create_chat([bot_partner.id])

        Bot = self.env["copywriting.matrix.bot"]
        self.assertTrue(
            Bot.apply_from_message(
                channel,
                self.env["mail.message"],
                {
                    "body": "help",
                    "author_id": user_partner.id,
                },
            )
        )
        messages = channel.message_ids.filtered(
            lambda m: m.author_id == bot_partner
        )
        self.assertTrue(messages)
        self.assertTrue(any("Content Matrix Bot" in (m.body or "") for m in messages))

        Bot.apply_from_message(
            channel,
            self.env["mail.message"],
            {
                "body": "start botsite",
                "author_id": user_partner.id,
            },
        )
        session = self.env["copywriting.session"].search(
            [
                ("website_id", "=", self.website.id),
                ("user_id", "=", self.env.user.id),
                ("state", "=", "intro"),
            ],
            limit=1,
        )
        self.assertTrue(session)
        self.assertEqual(session.discuss_channel_id, channel)

        Bot.apply_from_message(
            channel,
            self.env["mail.message"],
            {"body": "proceed", "author_id": user_partner.id},
        )
        session.invalidate_recordset()
        self.assertEqual(session.state, "page_select")

    def test_bot_combined_section_card(self):
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        session.action_start()
        session.action_proceed()
        session.current_page_id = self.page
        session.action_choose_page()
        session.action_bot_open_section_review()
        self.assertEqual(session.state, "section_decide")
        html = session._format_step_card_html(include_preview=True)
        self.assertIn("4.1 Fact", html)
        self.assertIn("4.2 Interpretation", html)
        self.assertIn("4.3 Suggestion", html)
        self.assertIn("Open in editor", html)
        self.assertIn("enable_editor=1", html)
        self.assertNotIn("target=\"_blank\"", html)
        self.assertIn("NEW", html)  # suggestion

    def test_quick_options_and_numeric_choice(self):
        Bot = self.env["copywriting.matrix.bot"]
        session = self.env["copywriting.session"].create(
            {"website_id": self.website.id}
        )
        session.action_start()
        html = Bot._with_options(
            "<p>intro</p>", session, self.env.user
        )
        self.assertIn("o_matrix_bot_choice", html)
        self.assertIn("#mxcmd=next", html)
        self.assertIn("Continue", html)
        # number maps to first option
        resolved = Bot._resolve_choice("1", session, self.env.user)
        self.assertEqual(resolved, "next")
