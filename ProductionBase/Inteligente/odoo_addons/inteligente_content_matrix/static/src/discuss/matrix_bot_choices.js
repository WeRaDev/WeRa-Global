/** @odoo-module **/

import { Message } from "@mail/core/common/message";
import { patch } from "@web/core/utils/patch";

/**
 * Content Matrix Bot message interactions:
 * - option chips → post command into Discuss thread
 * - editor deep-links → navigate/scroll the Website Edit iframe (not parent-only hash)
 */

function getWebsiteEditorIframe() {
    const candidates = [
        ...document.querySelectorAll(".o_website_preview iframe"),
        ...document.querySelectorAll(".o_iframe_container iframe"),
        ...document.querySelectorAll("iframe.o_iframe"),
        ...document.querySelectorAll("iframe"),
    ];
    for (const iframe of candidates) {
        try {
            const doc = iframe.contentDocument;
            if (!doc) {
                continue;
            }
            if (doc.getElementById("wrapwrap") || doc.getElementById("wrap") || doc.body) {
                return iframe;
            }
        } catch {
            // cross-origin
        }
    }
    return null;
}

function scrollToIdInDoc(doc, id) {
    if (!doc || !id) {
        return false;
    }
    let el = null;
    try {
        el = doc.getElementById(id);
    } catch {
        el = null;
    }
    if (!el) {
        try {
            el = doc.querySelector(`[id="${CSS.escape(id)}"]`);
        } catch {
            el = null;
        }
    }
    if (!el) {
        return false;
    }
    try {
        el.scrollIntoView({ behavior: "smooth", block: "center" });
    } catch {
        el.scrollIntoView(true);
    }
    const prevOutline = el.style.outline;
    const prevOffset = el.style.outlineOffset;
    el.style.outline = "3px solid #714B67";
    el.style.outlineOffset = "4px";
    setTimeout(() => {
        el.style.outline = prevOutline;
        el.style.outlineOffset = prevOffset;
    }, 1600);
    return true;
}

/**
 * Navigate Website Edit view to path?enable_editor=1#dom_id and scroll the block.
 * Prefer the builder iframe when present (Discuss lives in the parent shell).
 */
function navigateEditorTarget(href) {
    let target;
    try {
        target = new URL(href, window.location.origin);
    } catch {
        window.location.assign(href);
        return;
    }

    if (!target.searchParams.get("enable_editor")) {
        target.searchParams.set("enable_editor", "1");
    }
    const hashId = target.hash ? target.hash.replace(/^#/, "") : "";

    const iframe = getWebsiteEditorIframe();
    if (iframe && iframe.contentWindow) {
        const iwin = iframe.contentWindow;
        const idoc = iframe.contentDocument;
        let ipath = "/";
        try {
            ipath = iwin.location.pathname || "/";
        } catch {
            // ignore
        }

        const samePath =
            ipath === target.pathname ||
            (target.pathname === "/" && (ipath === "/" || ipath === ""));

        if (samePath && hashId && idoc) {
            if (scrollToIdInDoc(idoc, hashId)) {
                return;
            }
            try {
                iwin.location.hash = hashId;
            } catch {
                // ignore
            }
            setTimeout(() => scrollToIdInDoc(iframe.contentDocument, hashId), 150);
            setTimeout(() => scrollToIdInDoc(iframe.contentDocument, hashId), 500);
            return;
        }

        const next =
            target.pathname +
            "?" +
            target.searchParams.toString() +
            (hashId ? "#" + hashId : "");
        const onLoad = () => {
            iframe.removeEventListener("load", onLoad);
            setTimeout(() => scrollToIdInDoc(iframe.contentDocument, hashId), 50);
            setTimeout(() => scrollToIdInDoc(iframe.contentDocument, hashId), 300);
            setTimeout(() => scrollToIdInDoc(iframe.contentDocument, hashId), 800);
        };
        iframe.addEventListener("load", onLoad);
        try {
            iwin.location.assign(next);
        } catch {
            iframe.src = next;
        }
        return;
    }

    // No builder iframe: same-document frontend editor (or plain page)
    const cur = window.location;
    const sameDocPath =
        cur.pathname === target.pathname ||
        (target.pathname === "/" && (cur.pathname === "/" || cur.pathname === ""));

    if (sameDocPath && hashId) {
        if (!cur.searchParams.get("enable_editor")) {
            const next =
                target.pathname +
                "?" +
                target.searchParams.toString() +
                (hashId ? "#" + hashId : "");
            window.location.assign(next);
            return;
        }
        if (scrollToIdInDoc(document, hashId)) {
            if (cur.hash !== "#" + hashId) {
                cur.hash = hashId;
            }
            return;
        }
        cur.hash = hashId;
        setTimeout(() => scrollToIdInDoc(document, hashId), 150);
        setTimeout(() => scrollToIdInDoc(document, hashId), 500);
        return;
    }

    window.location.assign(
        target.pathname + "?" + target.searchParams.toString() + target.hash
    );
}

patch(Message.prototype, {
    async onClick(ev) {
        const preview = ev.target.closest?.(".o_matrix_preview_link");
        if (preview) {
            const href = preview.getAttribute("href");
            if (href) {
                ev.preventDefault();
                ev.stopPropagation();
                navigateEditorTarget(href);
            }
            return;
        }
        const choice = ev.target.closest?.(".o_matrix_bot_choice");
        if (choice) {
            ev.preventDefault();
            ev.stopPropagation();
            let cmd = "";
            const href = choice.getAttribute("href") || "";
            const m = href.match(/#mxcmd=([^&]*)/);
            if (m) {
                try {
                    cmd = decodeURIComponent(m[1] || "").trim();
                } catch {
                    cmd = (m[1] || "").trim();
                }
            }
            if (!cmd) {
                cmd = (choice.textContent || "").trim();
            }
            if (!cmd) {
                return;
            }
            const thread =
                this.props.message?.thread ||
                this.message?.thread ||
                this.props.thread;
            if (thread?.post) {
                await thread.post(cmd);
            }
            return;
        }
        return super.onClick(ev);
    },
});
