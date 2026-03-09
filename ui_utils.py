"""
ui_utils.py — Stili condivisi, widget e utilità UI
"""

import tkinter as tk
from tkinter import ttk

# ─────────────────────────────────────────────
# PALETTE COLORI
# ─────────────────────────────────────────────

COLORS = {
    # Sfondi
    "bg":           "#1E1E2E",
    "bg_card":      "#2A2A3E",
    "bg_bar":       "#181825",
    "bg_input":     "#2A2A3E",
    "bg_hover":     "#313244",
    "bg_selected":  "#45475A",

    # Testo
    "fg":           "#CDD6F4",
    "fg_dim":       "#6C7086",
    "fg_muted":     "#45475A",

    # Accenti — modalità italiana (verde/ambra)
    "accent_it":    "#A6E3A1",
    "accent_it2":   "#94E2D5",

    # Accenti — modalità latina (oro/viola)
    "accent_la":    "#F9E2AF",
    "accent_la2":   "#CBA6F7",
    "accent_gr":    "#89DCEB",   # azzurro per il greco antico

    # Comuni
    "purple":       "#CBA6F7",
    "red":          "#F38BA8",
    "green":        "#A6E3A1",
    "teal":         "#94E2D5",
    "yellow":       "#F9E2AF",
    "blue":         "#89DCEB",

    # Bordi
    "border":       "#45475A",
    "border_focus": "#CBA6F7",
}

FONTS = {
    "title":   ("Segoe UI", 14, "bold"),
    "label":   ("Segoe UI", 10, "bold"),
    "body":    ("Segoe UI", 11),
    "small":   ("Segoe UI", 9),
    "mono":    ("Consolas", 10),
    "status":  ("Segoe UI", 9),
    "tab":     ("Segoe UI", 10),
}


# ─────────────────────────────────────────────
# APPLY GLOBAL STYLES
# ─────────────────────────────────────────────

def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TNotebook",
                    background=COLORS["bg"], borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=COLORS["bg_card"], foreground=COLORS["fg"],
                    padding=[16, 8], font=FONTS["tab"])
    style.map("TNotebook.Tab",
              background=[("selected", COLORS["bg_hover"])],
              foreground=[("selected", COLORS["purple"])])

    style.configure("Treeview",
                    background=COLORS["bg_card"], foreground=COLORS["fg"],
                    fieldbackground=COLORS["bg_card"], rowheight=28,
                    font=FONTS["body"])
    style.configure("Treeview.Heading",
                    background=COLORS["bg_hover"], foreground=COLORS["purple"],
                    font=("Segoe UI", 10, "bold"))
    style.map("Treeview",
              background=[("selected", COLORS["bg_selected"])])

    style.configure("Vertical.TScrollbar",
                    background=COLORS["bg_card"], troughcolor=COLORS["bg"],
                    arrowcolor=COLORS["fg_dim"], borderwidth=0)

    style.configure("TCombobox",
                    fieldbackground=COLORS["bg_input"],
                    background=COLORS["bg_input"],
                    foreground=COLORS["fg"],
                    arrowcolor=COLORS["fg"],
                    selectbackground=COLORS["bg_selected"],
                    selectforeground=COLORS["fg"])
    style.map("TCombobox",
              fieldbackground=[("readonly", COLORS["bg_input"])],
              foreground=[("readonly", COLORS["fg"])])

    style.configure("TPanedwindow", background=COLORS["bg"])
    style.configure("Sash", sashthickness=6, background=COLORS["bg_hover"])


# ─────────────────────────────────────────────
# WIDGET HELPERS
# ─────────────────────────────────────────────

def label(parent, text, style="label", fg=None, **kwargs):
    return tk.Label(parent,
                    text=text,
                    bg=COLORS["bg"],
                    fg=fg or COLORS[{"label": "fg", "title": "purple", "dim": "fg_dim"}.get(style, "fg")],
                    font=FONTS.get(style, FONTS["body"]),
                    **kwargs)


def text_input(parent, height=3, **kwargs):
    w = tk.Text(parent, height=height,
                bg=COLORS["bg_input"], fg=COLORS["fg"],
                insertbackground=COLORS["fg"],
                relief="flat", font=FONTS["body"], wrap="word",
                bd=0, highlightthickness=1,
                highlightbackground=COLORS["border"],
                highlightcolor=COLORS["border_focus"],
                **kwargs)
    attach_text_ctx(w)
    return w


def entry_input(parent, textvariable=None, width=30, **kwargs):
    w = tk.Entry(parent,
                 textvariable=textvariable,
                 bg=COLORS["bg_input"], fg=COLORS["fg"],
                 insertbackground=COLORS["fg"],
                 relief="flat", font=FONTS["body"],
                 bd=0, highlightthickness=1,
                 highlightbackground=COLORS["border"],
                 highlightcolor=COLORS["border_focus"],
                 width=width, **kwargs)
    attach_entry_ctx(w)
    return w


def btn(parent, text, command, color="purple", **kwargs):
    bg_map = {
        "purple": (COLORS["purple"],  "#1E1E2E"),
        "green":  (COLORS["green"],   "#1E1E2E"),
        "teal":   (COLORS["teal"],    "#1E1E2E"),
        "yellow": (COLORS["yellow"],  "#1E1E2E"),
        "blue":   (COLORS["blue"],    "#1E1E2E"),
        "ghost":  (COLORS["bg_hover"], COLORS["fg"]),
        "danger": (COLORS["bg_hover"], COLORS["red"]),
    }
    bg, fg = bg_map.get(color, (COLORS["purple"], "#1E1E2E"))
    return tk.Button(parent, text=text, command=command,
                     bg=bg, fg=fg,
                     font=("Segoe UI", 10, "bold"),
                     relief="flat", padx=14, pady=7,
                     cursor="hand2",
                     activebackground=COLORS["bg_selected"],
                     activeforeground=fg,
                     **kwargs)


def section_title(parent, text, fg_key="purple"):
    f = tk.Frame(parent, bg=COLORS["bg"])
    f.pack(fill="x", padx=20, pady=(20, 2))
    tk.Label(f, text=text, bg=COLORS["bg"],
             fg=COLORS[fg_key], font=FONTS["title"]).pack(anchor="w")
    tk.Frame(f, bg=COLORS["border"], height=1).pack(fill="x", pady=(6, 0))


def scrolled_tree(parent, columns, headings, widths, height=8):
    """Crea un Treeview con scrollbar verticale."""
    frame = tk.Frame(parent, bg=COLORS["bg"])
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for col, head, w in zip(columns, headings, widths):
        tree.heading(col, text=head)
        tree.column(col, width=w, anchor="w")
    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set)
    tree.pack(side="left", fill="both", expand=True)
    sb.pack(side="left", fill="y")
    return frame, tree


# ─────────────────────────────────────────────
# CONTEXT MENUS
# ─────────────────────────────────────────────

def _make_ctx(widget, items):
    m = tk.Menu(widget, tearoff=0,
                bg=COLORS["bg_card"], fg=COLORS["fg"],
                activebackground=COLORS["bg_selected"],
                activeforeground=COLORS["fg"],
                relief="flat", bd=0)
    for item in items:
        if item == "---":
            m.add_separator()
        else:
            m.add_command(label=item[0], command=item[1])
    return m


def attach_text_ctx(widget):
    def show(e):
        m = _make_ctx(widget, [
            ("✂️  Taglia",      lambda: widget.event_generate("<<Cut>>")),
            ("📋 Copia",        lambda: widget.event_generate("<<Copy>>")),
            ("📌 Incolla",      lambda: widget.event_generate("<<Paste>>")),
            "---",
            ("Seleziona tutto", lambda: widget.tag_add("sel", "1.0", "end")),
        ])
        m.tk_popup(e.x_root, e.y_root)
    widget.bind("<Button-3>", show)


def attach_entry_ctx(widget):
    def show(e):
        m = _make_ctx(widget, [
            ("✂️  Taglia",      lambda: widget.event_generate("<<Cut>>")),
            ("📋 Copia",        lambda: widget.event_generate("<<Copy>>")),
            ("📌 Incolla",      lambda: widget.event_generate("<<Paste>>")),
            "---",
            ("Seleziona tutto", lambda: widget.select_range(0, "end")),
        ])
        m.tk_popup(e.x_root, e.y_root)
    widget.bind("<Button-3>", show)


def tree_ctx_menu(root, tree, on_copy_fields, on_delete):
    """
    Menu contestuale per Treeview.
    on_copy_fields: lista di (label, indice_colonna)
    on_delete: callable
    """
    def show(e):
        item = tree.identify_row(e.y)
        if not item:
            return
        tree.selection_set(item)
        vals = tree.item(item)["values"]
        items = []
        for lbl, idx in on_copy_fields:
            val = str(vals[idx]) if idx < len(vals) else ""
            items.append((lbl, lambda v=val: _clipboard_copy(root, v)))
        items.append("---")
        items.append(("🗑  Elimina", on_delete))
        m = _make_ctx(tree, items)
        m.tk_popup(e.x_root, e.y_root)
    tree.bind("<Button-3>", show)


def _clipboard_copy(root, text):
    root.clipboard_clear()
    root.clipboard_append(text)
