"""
tab_proverbi.py — Pannello completo per i Proverbi Italiani
Contiene i tre tab: Inserisci, Categorie, Ricerca
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import ui_utils as ui


class PannelloProverbi(tk.Frame):
    """Frame principale con notebook a 3 tab per i Proverbi Italiani."""

    def __init__(self, parent, status_cb, **kwargs):
        super().__init__(parent, bg=ui.COLORS["bg"], **kwargs)
        self.status_cb = status_cb  # callback per aggiornare la barra di stato
        self._build_notebook()

    # ─────────────────────────────────────────
    # NOTEBOOK
    # ─────────────────────────────────────────

    def _build_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.tab_ins  = tk.Frame(self.nb, bg=ui.COLORS["bg"])
        self.tab_cat  = tk.Frame(self.nb, bg=ui.COLORS["bg"])
        self.tab_ric  = tk.Frame(self.nb, bg=ui.COLORS["bg"])

        self.nb.add(self.tab_ins, text="  ✏️  Inserisci  ")
        self.nb.add(self.tab_cat, text="  📂  Categorie  ")
        self.nb.add(self.tab_ric, text="  🔍  Ricerca  ")

        self._build_inserisci()
        self._build_categorie()
        self._build_ricerca()

    # ─────────────────────────────────────────
    # TAB INSERISCI
    # ─────────────────────────────────────────

    def _build_inserisci(self):
        f = self.tab_ins
        ui.section_title(f, "Nuovo Proverbio", "accent_it")

        tk.Label(f, text="Testo del proverbio *",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", padx=20, pady=(12, 2))
        self.ins_testo = ui.text_input(f, height=3)
        self.ins_testo.pack(fill="x", padx=20)

        tk.Label(f, text="Significato / Spiegazione",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", padx=20, pady=(10, 2))
        self.ins_sig = ui.text_input(f, height=3)
        self.ins_sig.pack(fill="x", padx=20)

        row = tk.Frame(f, bg=ui.COLORS["bg"])
        row.pack(fill="x", padx=20, pady=(10, 4))
        tk.Label(row, text="Categoria:",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(side="left", padx=(0, 10))
        self.ins_cat_var = tk.StringVar()
        self.ins_cat_cb = ttk.Combobox(row, textvariable=self.ins_cat_var,
                                       state="readonly", width=28,
                                       font=ui.FONTS["body"])
        self.ins_cat_cb.pack(side="left")
        self._refresh_combo()

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=12)
        ui.btn(btn_row, "  💾  Salva", self._salva, color="green").pack(side="left", padx=(0, 8))
        ui.btn(btn_row, "  🗑  Pulisci", self._pulisci, color="ghost").pack(side="left")

        tk.Label(f, text="Ultimi inseriti",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg_dim"],
                 font=ui.FONTS["small"]).pack(anchor="w", padx=20)

        frame, self.ins_tree = ui.scrolled_tree(
            f,
            columns=("id", "testo", "categoria", "data"),
            headings=("#", "Proverbio", "Categoria", "Data"),
            widths=(40, 400, 150, 110),
            height=6
        )
        frame.pack(fill="x", padx=20, pady=(4, 10))
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.ins_tree,
            on_copy_fields=[("📋 Copia proverbio", 1)],
            on_delete=lambda: self._elimina_da_tree(self.ins_tree)
        )
        self._refresh_ins_tree()

    def _salva(self):
        testo = self.ins_testo.get("1.0", "end").strip()
        sig   = self.ins_sig.get("1.0", "end").strip()
        cat   = self.ins_cat_var.get()
        if not testo:
            messagebox.showwarning("Attenzione", "Il testo del proverbio è obbligatorio.")
            return
        cat_id = next((cid for cid, cnome in db.get_categorie() if cnome == cat), None)
        db.inserisci_proverbio(testo, sig, cat_id)
        self._pulisci()
        self._refresh_ins_tree()
        self._refresh_cat_tree()
        self.status_cb(f"Proverbio salvato ✅  ({db.count_proverbi()} totali)")
        messagebox.showinfo("Salvato", "Proverbio salvato con successo! ✅")

    def _pulisci(self):
        self.ins_testo.delete("1.0", "end")
        self.ins_sig.delete("1.0", "end")

    def _refresh_ins_tree(self):
        for r in self.ins_tree.get_children():
            self.ins_tree.delete(r)
        for p in db.get_proverbi()[:12]:
            t = p[1][:70] + "…" if len(p[1]) > 70 else p[1]
            self.ins_tree.insert("", "end", iid=str(p[0]),
                                 values=(p[0], t, p[3] or "—", p[4][:10]))

    def _refresh_combo(self):
        cats = [c[1] for c in db.get_categorie()]
        self.ins_cat_cb["values"] = cats
        if cats:
            self.ins_cat_cb.set(cats[0])

    # ─────────────────────────────────────────
    # TAB CATEGORIE
    # ─────────────────────────────────────────

    def _build_categorie(self):
        f = self.tab_cat
        ui.section_title(f, "Gestione Categorie", "accent_it")

        top = tk.Frame(f, bg=ui.COLORS["bg"])
        top.pack(fill="x", padx=20, pady=10)
        self.cat_var = tk.StringVar()
        e = ui.entry_input(top, textvariable=self.cat_var, width=28)
        e.pack(side="left", ipady=6, padx=(0, 10))
        e.bind("<Return>", lambda ev: self._aggiungi_cat())
        ui.btn(top, "  ➕  Aggiungi", self._aggiungi_cat, color="green").pack(side="left")

        paned = tk.PanedWindow(f, orient="horizontal", bg=ui.COLORS["bg"],
                               sashwidth=6, sashrelief="flat")
        paned.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        left = tk.Frame(paned, bg=ui.COLORS["bg"])
        paned.add(left, minsize=200)
        tk.Label(left, text="Categorie", bg=ui.COLORS["bg"],
                 fg=ui.COLORS["fg_dim"], font=ui.FONTS["small"]).pack(anchor="w")
        _, self.cat_tree = ui.scrolled_tree(
            left,
            columns=("id", "nome", "n"),
            headings=("#", "Nome", "N°"),
            widths=(40, 170, 45)
        )
        self.cat_tree.master.pack(fill="both", expand=True)
        self.cat_tree.bind("<<TreeviewSelect>>", self._on_cat_select)
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.cat_tree,
            on_copy_fields=[("📋 Copia nome", 1)],
            on_delete=self._elimina_cat
        )

        right = tk.Frame(paned, bg=ui.COLORS["bg"])
        paned.add(right, minsize=320)
        tk.Label(right, text="Proverbi nella categoria", bg=ui.COLORS["bg"],
                 fg=ui.COLORS["fg_dim"], font=ui.FONTS["small"]).pack(anchor="w")
        _, self.cat_prov_tree = ui.scrolled_tree(
            right,
            columns=("id", "testo", "significato"),
            headings=("#", "Proverbio", "Significato"),
            widths=(40, 230, 200)
        )
        self.cat_prov_tree.master.pack(fill="both", expand=True)
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.cat_prov_tree,
            on_copy_fields=[("📋 Copia proverbio", 1), ("📋 Copia significato", 2)],
            on_delete=lambda: self._elimina_da_tree(self.cat_prov_tree, db.elimina_proverbio)
        )

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=(0, 10))
        ui.btn(btn_row, "  🗑  Elimina categoria selezionata",
               self._elimina_cat, color="danger").pack(side="left")

        self._refresh_cat_tree()

    def _refresh_cat_tree(self):
        for r in self.cat_tree.get_children():
            self.cat_tree.delete(r)
        for row in db.get_cat_proverbi_stats():
            self.cat_tree.insert("", "end", iid=str(row[0]), values=row)

    def _on_cat_select(self, _event):
        sel = self.cat_tree.selection()
        if not sel:
            return
        cat_id = int(sel[0])
        for r in self.cat_prov_tree.get_children():
            self.cat_prov_tree.delete(r)
        for p in db.get_proverbi(cat_id):
            t = p[1][:60] + "…" if len(p[1]) > 60 else p[1]
            s = (p[2] or "")[:60] + "…" if p[2] and len(p[2]) > 60 else (p[2] or "")
            self.cat_prov_tree.insert("", "end", iid=str(p[0]), values=(p[0], t, s))

    def _aggiungi_cat(self):
        nome = self.cat_var.get().strip()
        if not nome:
            messagebox.showwarning("Attenzione", "Inserisci il nome della categoria.")
            return
        db.inserisci_categoria(nome)
        self.cat_var.set("")
        self._refresh_cat_tree()
        self._refresh_combo()
        self.status_cb("Categoria aggiunta ✅")

    def _elimina_cat(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona una categoria da eliminare.")
            return
        cat_id = int(sel[0])
        nome = self.cat_tree.item(sel[0])["values"][1]
        if messagebox.askyesno("Conferma",
                               f"Eliminare la categoria «{nome}»?\n"
                               "I proverbi associati perderanno la categoria."):
            db.elimina_categoria(cat_id)
            self._refresh_cat_tree()
            self._refresh_combo()
            self.status_cb("Categoria eliminata")

    # ─────────────────────────────────────────
    # TAB RICERCA
    # ─────────────────────────────────────────

    def _build_ricerca(self):
        f = self.tab_ric
        ui.section_title(f, "Cerca Proverbi", "accent_it")

        top = tk.Frame(f, bg=ui.COLORS["bg"])
        top.pack(fill="x", padx=20, pady=10)
        self.ric_var = tk.StringVar()
        e = ui.entry_input(top, textvariable=self.ric_var, width=38)
        e.pack(side="left", ipady=8, padx=(0, 10))
        e.bind("<Return>", lambda ev: self._cerca())
        ui.btn(top, "  🔍  Cerca", self._cerca, color="teal").pack(side="left", padx=(0, 8))
        ui.btn(top, "Tutti", self._mostra_tutti, color="ghost").pack(side="left")

        self.ric_info = tk.Label(f, text="", bg=ui.COLORS["bg"],
                                 fg=ui.COLORS["fg_dim"], font=ui.FONTS["small"])
        self.ric_info.pack(anchor="w", padx=20)

        frame, self.ric_tree = ui.scrolled_tree(
            f,
            columns=("id", "testo", "significato", "categoria", "data"),
            headings=("#", "Proverbio", "Significato", "Categoria", "Data"),
            widths=(40, 250, 230, 130, 100)
        )
        frame.pack(fill="both", expand=True, padx=20, pady=(4, 0))
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.ric_tree,
            on_copy_fields=[("📋 Copia proverbio", 1), ("📋 Copia significato", 2)],
            on_delete=lambda: self._elimina_da_tree(self.ric_tree, db.elimina_proverbio)
        )

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=8)
        ui.btn(btn_row, "  🗑  Elimina selezionato",
               lambda: self._elimina_da_tree(self.ric_tree, db.elimina_proverbio),
               color="danger").pack(side="left")

        self._mostra_tutti()

    def _cerca(self):
        q = self.ric_var.get().strip()
        if not q:
            self._mostra_tutti()
            return
        risultati = db.cerca_proverbi(q)
        self._popola_ric(risultati)
        self.ric_info.config(text=f"{len(risultati)} risultati per «{q}»")

    def _mostra_tutti(self):
        tutti = db.get_proverbi()
        self._popola_ric(tutti)
        self.ric_info.config(text=f"Tutti i proverbi: {len(tutti)}")

    def _popola_ric(self, rows):
        for r in self.ric_tree.get_children():
            self.ric_tree.delete(r)
        for p in rows:
            t = p[1][:55] + "…" if len(p[1]) > 55 else p[1]
            s = (p[2] or "")[:55] + "…" if p[2] and len(p[2]) > 55 else (p[2] or "")
            self.ric_tree.insert("", "end", iid=str(p[0]),
                                 values=(p[0], t, s, p[3] or "—", p[4][:10]))

    # ─────────────────────────────────────────
    # UTILITY
    # ─────────────────────────────────────────

    def _elimina_da_tree(self, tree, delete_fn=None):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona un elemento da eliminare.")
            return
        pid = int(sel[0])
        testo = str(tree.item(sel[0])["values"][1])
        if messagebox.askyesno("Conferma eliminazione",
                               f"Eliminare:\n«{testo}»?"):
            if delete_fn:
                delete_fn(pid)
            tree.delete(sel[0])
            self._refresh_ins_tree()
            self._refresh_cat_tree()
            self.status_cb(f"Eliminato  •  {db.count_proverbi()} proverbi rimasti")

    def vai_inserisci(self):
        self.nb.select(0)

    def vai_ricerca(self):
        self.nb.select(2)
