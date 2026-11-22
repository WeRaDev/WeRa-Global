# -*- coding: utf-8 -*-
"""Auth-only Discuss adapter driving copywriting.session (Content Matrix Bot)."""
import logging
import re
from html import escape

from markupsafe import Markup

from odoo import models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

HELP_TEXT = (
    "<p><b>Content Matrix Bot</b> (operators only)</p>"
    "<p>Use the <b>option buttons</b> under each reply, or type a number / short command.</p>"
    "<p>Typed commands still work: "
    "<code>help</code>, <code>start [code]</code>, <code>next</code>, "
    "<code>pages</code>, <code>page &lt;name&gt;</code>, <code>sections</code>, "
    "<code>accept</code>, <code>edit &lt;text&gt;</code>, "
    "<code>reject &lt;note&gt;</code>, <code>skip</code>, "
    "<code>pause</code>, <code>resume</code>, <code>finish</code>, "
    "<code>preview</code>.</p>"
    "<p><b>Open in editor</b> uses Website Edit links "
    "(<code>?enable_editor=1</code> ± <code>#dom_id</code>) in the same window.</p>"
)


class MatrixDiscussBotLogic(models.AbstractModel):
    _name = "copywriting.matrix.bot"
    _description = "Content Matrix Discuss Bot Logic"

    def _bot_partner(self):
        return self.env.ref(
            "inteligente_content_matrix.partner_matrix_bot", raise_if_not_found=False
        )

    def _user_allowed(self, user):
        return user.has_group(
            "inteligente_content_matrix.group_operator"
        ) or user.has_group("inteligente_content_matrix.group_manager")

    def _strip_html(self, body):
        if not body:
            return ""
        text = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
        text = re.sub(r"<[^>]+>", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def _is_bot_author(self, author_id):
        bot = self._bot_partner()
        return bool(bot and author_id == bot.id)

    def _channel_has_bot(self, channel):
        bot = self._bot_partner()
        if not bot:
            return False
        partners = channel.channel_partner_ids if "channel_partner_ids" in channel._fields else channel.channel_member_ids.mapped("partner_id")
        return bot in partners

    def _is_bot_pinged(self, msg_vals):
        bot = self._bot_partner()
        if not bot:
            return False
        partner_ids = msg_vals.get("partner_ids") or []
        if partner_ids and isinstance(partner_ids[0], (list, tuple)):
            # commands like (6, 0, ids)
            flat = []
            for item in partner_ids:
                if isinstance(item, (list, tuple)) and len(item) >= 3 and item[0] == 6:
                    flat.extend(item[2] or [])
                elif isinstance(item, int):
                    flat.append(item)
            partner_ids = flat
        return bot.id in partner_ids

    def _find_session_for_channel(self, channel, user):
        Session = self.env["copywriting.session"]
        bound = Session.search(
            [
                ("discuss_channel_id", "=", channel.id),
                ("user_id", "=", user.id),
                ("state", "not in", ("finished",)),
            ],
            limit=1,
        )
        if bound:
            return bound
        return Session.search(
            [
                ("user_id", "=", user.id),
                ("state", "not in", ("finished", "draft")),
            ],
            limit=1,
        )

    def _bind_channel(self, session, channel):
        if session.discuss_channel_id != channel:
            session.discuss_channel_id = channel.id

    def _post(self, channel, body_html):
        bot = self._bot_partner()
        if not bot:
            return
        channel.with_context(
            mail_create_nosubscribe=True,
            matrix_bot_skip=True,
        ).sudo().message_post(
            body=Markup(body_html),
            message_type="comment",
            subtype_xmlid="mail.mt_comment",
            author_id=bot.id,
        )

    def apply_from_message(self, channel, message, msg_vals):
        """Entry from discuss.channel hook. Returns True if handled."""
        if self.env.context.get("matrix_bot_skip"):
            return False
        bot = self._bot_partner()
        if not bot:
            return False
        author_id = msg_vals.get("author_id") or (
            message.author_id.id if message else False
        )
        if self._is_bot_author(author_id):
            return False
        if not self._channel_has_bot(channel):
            return False
        # DM with bot always; group channels only when @mentioned
        is_dm = channel.channel_type == "chat"
        if not is_dm and not self._is_bot_pinged(msg_vals):
            return False

        user = self.env.user
        if user._is_public() or user.share:
            self._post(channel, "<p>Sign in as an internal user with Content Matrix access.</p>")
            return True
        if not self._user_allowed(user):
            self._post(
                channel,
                "<p>Access denied. You need the <b>Content Matrix / Operator</b> group.</p>",
            )
            return True

        body = self._strip_html(msg_vals.get("body") or (message.body if message else ""))
        # strip @BotName prefix
        body = re.sub(r"^@\S+\s*", "", body).strip()
        if not body:
            return False

        # Map bare numbers / labels to commands from current session options
        session_hint = self._find_session_for_channel(channel, user)
        body = self._resolve_choice(body, session_hint, user)

        try:
            reply = self._handle_command(channel, user, body)
        except (UserError, ValidationError) as err:
            reply = "<p><b>Error:</b> %s</p>" % escape(str(err))
        except Exception:
            _logger.exception("Matrix bot failed")
            reply = "<p>Something went wrong handling that command.</p>"

        if reply:
            self._post(channel, reply)
            return True
        return False

    def _handle_command(self, channel, user, body):
        lower = body.lower()
        parts = body.split(None, 1)
        cmd = parts[0].lower()
        arg = parts[1].strip() if len(parts) > 1 else ""

        if cmd in ("help", "?"):
            return self._with_options(HELP_TEXT, None, user, idle=True)

        session = self._find_session_for_channel(channel, user)

        if cmd == "start":
            return self._cmd_start(channel, user, arg, session)
        if cmd == "status":
            if not session:
                return self._with_options(
                    "<p>No active session.</p>", None, user, idle=True
                )
            self._bind_channel(session, channel)
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "preview":
            if not session:
                return self._with_options(
                    "<p>No active session.</p>", None, user, idle=True
                )
            self._bind_channel(session, channel)
            url = session.get_preview_url(editor=True) or ""
            body = (
                "<p><b>Open in Website Editor</b> (same window):</p>"
                '<p><a class="o_matrix_preview_link" href="%s">%s</a></p>'
                "<p style=\"color:#666;\">Uses <code>enable_editor=1</code> so you stay in edit mode with the chat.</p>"
                % (escape(url, quote=True), escape(url))
            )
            return self._with_options(body, session, user)
        if cmd == "pages":
            if not session:
                return self._with_options(
                    "<p>No active session.</p>", None, user, idle=True
                )
            self._bind_channel(session, channel)
            return self._with_options(self._format_pages(session), session, user)

        if not session and cmd not in ("start", "help"):
            return self._with_options(
                "<p>No active session. Tap <b>Start review</b> or type "
                "<code>start incity</code>.</p>",
                None,
                user,
                idle=True,
            )

        if session:
            self._bind_channel(session, channel)

        # Mutating commands
        if cmd in ("proceed", "next"):
            if session.state == "intro":
                session.action_proceed()
            elif session.state == "page_intro":
                return self._bot_start_section_review(session, user)
            elif session.state in (
                "section_fact",
                "section_interpret",
                "section_suggest",
                "section_decide",
            ):
                # Intermediate next collapses to combined decide (or stay on decide)
                session.action_bot_open_section_review()
            else:
                return self._with_options(
                    "<p><code>next</code> is not valid in state <b>%s</b>.</p>"
                    % escape(session.state),
                    session,
                    user,
                )
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )

        if cmd == "page":
            return self._cmd_page(session, arg, user)
        if cmd == "sections":
            return self._bot_start_section_review(session, user)
        if cmd == "accept":
            session.action_accept_suggestion()
            # After accept, jump next section straight to combined decide card
            if session.state == "section_fact":
                session.action_bot_open_section_review()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "edit":
            if not arg:
                return self._with_options(
                    "<p>Type the final text as: <code>edit your final copy here</code></p>",
                    session,
                    user,
                )
            if session.state != "section_decide":
                session.action_bot_open_section_review()
            session.action_enable_edit_mode()
            if session.current_section_id:
                session.current_section_id.content_final = arg
            session.action_save_edit()
            if session.state == "section_fact":
                session.action_bot_open_section_review()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "reject":
            if not arg:
                return self._with_options(
                    "<p>Type a reason as: <code>reject note about the issue</code></p>",
                    session,
                    user,
                )
            if session.state != "section_decide":
                session.action_bot_open_section_review()
            session.reject_note = arg
            session.action_reject_interpretation()
            # reject returns to interpret — bump back to combined decide for bot
            if session.state in (
                "section_interpret",
                "section_fact",
                "section_suggest",
            ):
                session.action_bot_open_section_review()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "skip":
            if session.state in (
                "section_fact",
                "section_interpret",
                "section_suggest",
            ):
                session.action_bot_open_section_review()
            session.action_skip_section()
            if session.state == "section_fact":
                session.action_bot_open_section_review()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "pause":
            session.action_later()
            return self._with_options(
                "<p>Session paused.</p>", session, user
            )
        if cmd == "resume":
            session.action_resume()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )
        if cmd == "finish":
            session.action_finish()
            return self._with_options(
                "<p>Session <b>finished</b>. Export matrix and run verify/apply when ready.</p>",
                None,
                user,
                idle=True,
            )
        if cmd == "nextpage":
            session.action_next_page()
            return self._with_options(
                session._format_step_card_html(include_preview=True), session, user
            )

        return self._with_options(
            "<p>Unknown option <code>%s</code>.</p>" % escape(cmd),
            session,
            user,
        )

    def _cmd_start(self, channel, user, website_code, session):
        Website = self.env["copywriting.website"]
        if session and session.state == "paused":
            self._bind_channel(session, channel)
            session.action_resume()
            return self._with_options(
                "<p>Resumed paused session.</p>"
                + session._format_step_card_html(include_preview=True),
                session,
                user,
            )
        if session and session.state not in ("draft", "finished"):
            self._bind_channel(session, channel)
            return self._with_options(
                "<p>You already have an active session.</p>"
                + session._format_step_card_html(include_preview=True),
                session,
                user,
            )

        code = (website_code or "").strip()
        if code:
            website = Website.search([("code", "=", code), ("active", "=", True)], limit=1)
            if not website:
                return self._with_options(
                    "<p>Unknown website code <code>%s</code>.</p>" % escape(code),
                    None,
                    user,
                    idle=True,
                )
        else:
            website = Website.search([("active", "=", True)], limit=1)
            if not website:
                return self._with_options(
                    "<p>No content-matrix website configured.</p>",
                    None,
                    user,
                    idle=True,
                )

        Session = self.env["copywriting.session"]
        if session and session.state == "draft" and session.website_id == website:
            new_session = session
        else:
            new_session = Session.create(
                {
                    "website_id": website.id,
                    "user_id": user.id,
                }
            )
        self._bind_channel(new_session, channel)
        new_session.action_start()
        body = (
            "<p>Started session for <b>%s</b>.</p>"
            % escape(website.name or website.code)
            + new_session._format_step_card_html(include_preview=True)
        )
        return self._with_options(body, new_session, user)

    def _bot_start_section_review(self, session, user):
        """Open first/current section as one combined decide card."""
        pending = session._pending_sections_for_page(session.current_page_id)
        if session.state == "page_intro" and not pending:
            page = session.current_page_id
            msg = (
                "<p><b>No open sections</b> on %s — nothing left to walk.</p>"
                "<p>All blocks are already approved, updated, or skipped.</p>"
                % escape(page.name or page.url or "this page")
            )
            if page:
                page.status = "done"
            session.write(
                {
                    "state": "page_done",
                    "current_section_id": False,
                    "edit_mode": False,
                    "reject_note": False,
                }
            )
            session._log_event("page_done", note="no pending sections on start")
            return self._with_options(
                msg + session._format_step_card_html(include_preview=True),
                session,
                user,
            )
        session.action_bot_open_section_review()
        return self._with_options(
            session._format_step_card_html(include_preview=True), session, user
        )

    def _cmd_page(self, session, arg, user):
        if not arg:
            return self._with_options(
                "<p>Pick a page with the buttons below, or type "
                "<code>page Home</code>.</p>",
                session,
                user,
            )
        pages = session._scope_pages()
        needle = arg.strip().lower()
        match = pages.filtered(
            lambda p: (p.url or "").lower() == needle
            or (p.name or "").lower() == needle
            or needle in (p.name or "").lower()
            or needle in (p.url or "").lower()
        )[:1]
        if not match:
            return self._with_options(
                "<p>Page not found in scope.</p>", session, user
            )
        if session.state == "page_done":
            session.action_next_page()
        session._require_state("page_select")
        session.current_page_id = match.id
        session.action_choose_page()
        return self._with_options(
            session._format_step_card_html(include_preview=True), session, user
        )

    def _format_pages(self, session):
        pages = session._scope_pages()
        if not pages:
            return "<p>No pages in scope.</p>"
        items = "".join(
            "<li><code>%s</code> — %s (%s)</li>"
            % (escape(p.url or "/"), escape(p.name or ""), escape(p.status or ""))
            for p in pages
        )
        return (
            "<p><b>Pages in scope</b></p><ul>%s</ul>"
            "<p>Tap a page button below (or type the number).</p>" % items
        )

    def _options_for(self, session, user, idle=False):
        """Return list of (command_string, label) for current context."""
        opts = []
        if idle or not session or session.state in ("finished",):
            opts.append(("start incity", "Start review (incity)"))
            opts.append(("help", "Help"))
            return opts

        state = session.state
        is_manager = user.has_group("inteligente_content_matrix.group_manager")

        if state == "intro":
            opts.append(("next", "Continue"))
            opts.append(("pause", "Pause"))
        elif state == "page_select":
            pages = session._scope_pages()
            # Prefer pages with pending work first (up to 12)
            ranked = sorted(
                pages,
                key=lambda p: (
                    0 if session._pending_sections_for_page(p) else 1,
                    p.sequence,
                    p.id,
                ),
            )[:12]
            for page in ranked:
                pending_n = len(session._pending_sections_for_page(page))
                label = page.name or page.url or "page"
                if pending_n:
                    label = "%s (%s open)" % (label, pending_n)
                else:
                    label = "%s (done)" % label
                target = page.url or page.name
                opts.append(("page %s" % target, "Open: %s" % label))
            opts.append(("status", "Status"))
            opts.append(("pause", "Pause"))
        elif state == "page_intro":
            pending = session._pending_sections_for_page(session.current_page_id)
            if pending:
                opts.append(("sections", "Start sections (%s open)" % len(pending)))
            else:
                opts.append(("nextpage", "Choose another page"))
                opts.append(("finish", "Finish session"))
            opts.append(("pause", "Pause"))
        elif state in (
            "section_fact",
            "section_interpret",
            "section_suggest",
            "section_decide",
        ):
            # Combined review card: decide immediately (no multi-step Next).
            opts.append(("accept", "Accept suggestion"))
            opts.append(("preview", "Open in editor"))
            if is_manager:
                opts.append(("skip", "Skip section"))
            opts.append(("pause", "Pause"))
            # edit/reject still need free text
        elif state == "page_done":
            opts.append(("nextpage", "Choose another page"))
            opts.append(("finish", "Finish session"))
            opts.append(("pause", "Pause"))
        elif state == "paused":
            opts.append(("resume", "Resume"))
            opts.append(("status", "Status"))
        else:
            opts.append(("status", "Status"))
            opts.append(("help", "Help"))

        opts.append(("help", "Help"))
        # de-dupe labels while keeping order
        seen = set()
        unique = []
        for cmd, label in opts:
            key = (cmd, label)
            if key in seen:
                continue
            seen.add(key)
            unique.append((cmd, label))
        return unique

    def _format_options_html(self, options):
        if not options:
            return ""
        from urllib.parse import quote

        # Prefer a plain numbered list: always visible in Discuss even if
        # Bootstrap btn styles fail to load; keep clickable #mxcmd links.
        items = []
        for idx, (cmd, label) in enumerate(options, start=1):
            href = "#mxcmd=%s" % quote(cmd or "", safe="")
            items.append(
                "<li value=\"%s\" style=\"margin:6px 0;\">"
                "<a href=\"%s\" class=\"o_matrix_bot_choice\" "
                "style=\"font-weight:600;\">%s</a>"
                " <span style=\"color:#666;\">(reply <code>%s</code>)</span>"
                "</li>"
                % (idx, escape(href, quote=True), escape(label), idx)
            )
        return (
            '<div class="o_matrix_bot_choices" '
            'style="margin-top:12px;padding:10px 12px;border:1px solid #d8d8d8;'
            'border-radius:6px;background:#f8f9fa;">'
            '<p style="margin:0 0 8px 0;"><b>What do you want to do?</b></p>'
            '<ol style="margin:0;padding-left:22px;">' 
            + "".join(items)
            + "</ol>"
            '<p style="margin:8px 0 0 0;color:#666;font-size:12px;">'
            "Click a line, or type its number.</p>"
            "</div>"
        )

    def _with_options(self, body_html, session, user, idle=False):
        opts = self._options_for(session, user, idle=idle)
        # Special case: decide step free-text hints
        extra = ""
        if session and session.state == "section_decide":
            extra = (
                "<p class=\"mt-2\">To change copy: type "
                "<code>edit your final text</code>. "
                "To reject interpretation: "
                "<code>reject reason here</code>.</p>"
            )
        return (body_html or "") + extra + self._format_options_html(opts)

    def _resolve_choice(self, body, session, user):
        """Map '1' / exact option label to the underlying command string."""
        text = (body or "").strip()
        if not text:
            return body
        opts = self._options_for(session, user, idle=not session)
        # pure number
        if re.fullmatch(r"\d+", text):
            idx = int(text) - 1
            if 0 <= idx < len(opts):
                return opts[idx][0]
        # exact label (case-insensitive)
        low = text.lower()
        for cmd, label in opts:
            if low == (label or "").lower() or low == (cmd or "").lower():
                return cmd
        # "1 · Continue" style from button visible text if user pasted it
        m = re.match(r"^(\d+)\s*[·.\-]\s*(.+)$", text)
        if m:
            idx = int(m.group(1)) - 1
            if 0 <= idx < len(opts):
                return opts[idx][0]
        return body


class DiscussChannelMatrixBot(models.Model):
    _inherit = "discuss.channel"

    def _message_post_after_hook(self, message, msg_vals):
        res = super()._message_post_after_hook(message, msg_vals)
        if self.env.context.get("matrix_bot_skip"):
            return res
        try:
            self.env["copywriting.matrix.bot"].apply_from_message(
                self, message, msg_vals or {}
            )
        except Exception:
            _logger.exception("Matrix bot hook failed")
        return res
