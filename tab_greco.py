"""
tab_latino.py — Pannello completo per le Frasi Greco Antico
Contiene i tre tab: Inserisci, Categorie, Ricerca
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import ui_utils as ui


class PannelloGreco(tk.Frame):
    """Frame principale con notebook a 3 tab per le Frasi Greco Antico."""

    def __init__(self, parent, status_cb, **kwargs):
        super().__init__(parent, bg=ui.COLORS["bg"], **kwargs)
        self.status_cb = status_cb
        self._build_notebook()

    # ─────────────────────────────────────────
    # NOTEBOOK
    # ─────────────────────────────────────────

    def _build_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self.tab_ins = tk.Frame(self.nb, bg=ui.COLORS["bg"])
        self.tab_cat = tk.Frame(self.nb, bg=ui.COLORS["bg"])
        self.tab_ric = tk.Frame(self.nb, bg=ui.COLORS["bg"])

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
        ui.section_title(f, "Nuova Frase Greca", "accent_gr")

        # Testo latino
        tk.Label(f, text="Frase in Greco Antico *",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", padx=20, pady=(12, 2))
        self.ins_testo = ui.text_input(f, height=2)
        self.ins_testo.pack(fill="x", padx=20)

        # Due colonne: traduzione + autore
        row2 = tk.Frame(f, bg=ui.COLORS["bg"])
        row2.pack(fill="x", padx=20, pady=(10, 0))

        left2 = tk.Frame(row2, bg=ui.COLORS["bg"])
        left2.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(left2, text="Traduzione italiana",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", pady=(0, 2))
        self.ins_trasl = ui.text_input(left2, height=2)
        self.ins_trasl.pack(fill="x")

        right2 = tk.Frame(row2, bg=ui.COLORS["bg"])
        right2.pack(side="left", fill="x", expand=True)
        tk.Label(right2, text="Autore",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", pady=(0, 2))
        self.ins_autore = ui.entry_input(right2, width=24)
        self.ins_autore.pack(fill="x", ipady=6)

        # Significato
        tk.Label(f, text="Significato / Commento",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(anchor="w", padx=20, pady=(10, 2))
        self.ins_sig = ui.text_input(f, height=3)
        self.ins_sig.pack(fill="x", padx=20)

        # Categoria
        row3 = tk.Frame(f, bg=ui.COLORS["bg"])
        row3.pack(fill="x", padx=20, pady=(10, 4))
        tk.Label(row3, text="Categoria:",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg"],
                 font=ui.FONTS["label"]).pack(side="left", padx=(0, 10))
        self.ins_cat_var = tk.StringVar()
        self.ins_cat_cb = ttk.Combobox(row3, textvariable=self.ins_cat_var,
                                       state="readonly", width=28,
                                       font=ui.FONTS["body"])
        self.ins_cat_cb.pack(side="left")
        self._refresh_combo()

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=10)
        ui.btn(btn_row, "  💾  Salva", self._salva, color="teal").pack(side="left", padx=(0, 8))
        ui.btn(btn_row, "  🗑  Pulisci", self._pulisci, color="ghost").pack(side="left")

        tk.Label(f, text="Ultime inserite",
                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg_dim"],
                 font=ui.FONTS["small"]).pack(anchor="w", padx=20)

        frame, self.ins_tree = ui.scrolled_tree(
            f,
            columns=("id", "testo", "traslitterazione", "traduzione", "autore", "categoria"),
            headings=("#", "Frase Greca", "Traslitterazione", "Traduzione", "Autore", "Categoria"),
            widths=(40, 200, 160, 160, 100, 100),
            height=5
        )
        frame.pack(fill="x", padx=20, pady=(4, 10))
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.ins_tree,
            on_copy_fields=[
                ("📋 Copia frase greca", 1),
                ("📋 Copia traduzione",   2),
            ],
            on_delete=lambda: self._elimina_da_tree(self.ins_tree)
        )
        self._refresh_ins_tree()

    def _salva(self):
        testo   = self.ins_testo.get("1.0", "end").strip()
        trad    = self.ins_trad.get("1.0", "end").strip()
        sig     = self.ins_sig.get("1.0", "end").strip()
        autore  = self.ins_autore.get().strip()
        cat     = self.ins_cat_var.get()

        if not testo:
            messagebox.showwarning("Attenzione", "La frase greca è obbligatoria.")
            return
        cat_id = next((cid for cid, cnome in db.get_categorie_greco() if cnome == cat), None)
        db.inserisci_frase_greco(testo, trad, sig, autore, cat_id)
        self._pulisci()
        self._refresh_ins_tree()
        self._refresh_cat_tree()
        self.status_cb(f"frase greca salvata ✅  ({db.count_frasi_greco()} totali)")
        messagebox.showinfo("Salvato", "frase greca salvata con successo! ✅")

    def _pulisci(self):
        self.ins_testo.delete("1.0", "end")
        self.ins_trad.delete("1.0", "end")
        self.ins_sig.delete("1.0", "end")
        self.ins_autore.delete(0, "end")

    def _refresh_ins_tree(self):
        for r in self.ins_tree.get_children():
            self.ins_tree.delete(r)
        for f in db.get_frasi_greco()[:12]:
            t = f[1][:55] + "…" if len(f[1]) > 55 else f[1]
            tr = (f[2] or "")[:55] + "…" if f[2] and len(f[2]) > 55 else (f[2] or "")
            self.ins_tree.insert("", "end", iid=str(f[0]),
                                 values=(f[0], t, tr, f[4] or "—", f[5] or "—"))

    def _refresh_combo(self):
        cats = [c[1] for c in db.get_categorie_greco()]
        self.ins_cat_cb["values"] = cats
        if cats:
            self.ins_cat_cb.set(cats[0])

    # ─────────────────────────────────────────
    # TAB CATEGORIE
    # ─────────────────────────────────────────

    def _build_categorie(self):
        f = self.tab_cat
        ui.section_title(f, "Gestione Categorie (Latino)", "accent_gr")

        top = tk.Frame(f, bg=ui.COLORS["bg"])
        top.pack(fill="x", padx=20, pady=10)
        self.cat_var = tk.StringVar()
        e = ui.entry_input(top, textvariable=self.cat_var, width=28)
        e.pack(side="left", ipady=6, padx=(0, 10))
        e.bind("<Return>", lambda ev: self._aggiungi_cat())
        ui.btn(top, "  ➕  Aggiungi", self._aggiungi_cat, color="teal").pack(side="left")

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
        tk.Label(right, text="Frasi nella categoria", bg=ui.COLORS["bg"],
                 fg=ui.COLORS["fg_dim"], font=ui.FONTS["small"]).pack(anchor="w")
        _, self.cat_frasi_tree = ui.scrolled_tree(
            right,
            columns=("id", "testo", "autore"),
            headings=("#", "frase greca", "Autore"),
            widths=(40, 310, 110)
        )
        self.cat_frasi_tree.master.pack(fill="both", expand=True)
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.cat_frasi_tree,
            on_copy_fields=[("📋 Copia frase", 1)],
            on_delete=lambda: self._elimina_da_tree(self.cat_frasi_tree)
        )

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=(0, 10))
        ui.btn(btn_row, "  🗑  Elimina categoria selezionata",
               self._elimina_cat, color="danger").pack(side="left")

        self._refresh_cat_tree()

    def _refresh_cat_tree(self):
        for r in self.cat_tree.get_children():
            self.cat_tree.delete(r)
        for row in db.get_cat_greco_stats():
            self.cat_tree.insert("", "end", iid=str(row[0]), values=row)

    def _on_cat_select(self, _event):
        sel = self.cat_tree.selection()
        if not sel:
            return
        cat_id = int(sel[0])
        for r in self.cat_frasi_tree.get_children():
            self.cat_frasi_tree.delete(r)
        for frase in db.get_frasi_greco(cat_id):
            t = frase[1][:70] + "…" if len(frase[1]) > 70 else frase[1]
            self.cat_frasi_tree.insert("", "end", iid=str(frase[0]),
                                       values=(frase[0], t, frase[4] or "—"))

    def _aggiungi_cat(self):
        nome = self.cat_var.get().strip()
        if not nome:
            messagebox.showwarning("Attenzione", "Inserisci il nome della categoria.")
            return
        db.inserisci_categoria_greco(nome)
        self.cat_var.set("")
        self._refresh_cat_tree()
        self._refresh_combo()
        self.status_cb("Categoria latina aggiunta ✅")

    def _elimina_cat(self):
        sel = self.cat_tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona una categoria da eliminare.")
            return
        cat_id = int(sel[0])
        nome = self.cat_tree.item(sel[0])["values"][1]
        if messagebox.askyesno("Conferma",
                               f"Eliminare la categoria «{nome}»?\n"
                               "Le frasi associate perderanno la categoria."):
            db.elimina_categoria_greco(cat_id)
            self._refresh_cat_tree()
            self._refresh_combo()
            self.status_cb("Categoria eliminata")

    # ─────────────────────────────────────────
    # TAB RICERCA
    # ─────────────────────────────────────────

    def _build_ricerca(self):
        f = self.tab_ric
        ui.section_title(f, "Cerca Frasi Greco Antico", "accent_gr")

        top = tk.Frame(f, bg=ui.COLORS["bg"])
        top.pack(fill="x", padx=20, pady=10)
        self.ric_var = tk.StringVar()
        e = ui.entry_input(top, textvariable=self.ric_var, width=38)
        e.pack(side="left", ipady=8, padx=(0, 10))
        e.bind("<Return>", lambda ev: self._cerca())
        ui.btn(top, "  🔍  Cerca", self._cerca, color="blue").pack(side="left", padx=(0, 8))
        ui.btn(top, "Tutte", self._mostra_tutte, color="ghost").pack(side="left")

        self.ric_info = tk.Label(f, text="", bg=ui.COLORS["bg"],
                                 fg=ui.COLORS["fg_dim"], font=ui.FONTS["small"])
        self.ric_info.pack(anchor="w", padx=20)

        frame, self.ric_tree = ui.scrolled_tree(
            f,
            columns=("id", "testo", "traduzione", "autore", "categoria", "data"),
            headings=("#", "frase greca", "Traduzione", "Autore", "Categoria", "Data"),
            widths=(40, 200, 180, 100, 110, 90)
        )
        frame.pack(fill="both", expand=True, padx=20, pady=(4, 0))
        ui.tree_ctx_menu(
            self.winfo_toplevel(), self.ric_tree,
            on_copy_fields=[
                ("📋 Copia frase greca", 1),
                ("📋 Copia traduzione",   2),
            ],
            on_delete=lambda: self._elimina_da_tree(self.ric_tree)
        )

        btn_row = tk.Frame(f, bg=ui.COLORS["bg"])
        btn_row.pack(anchor="w", padx=20, pady=8)
        ui.btn(btn_row, "  🗑  Elimina selezionata",
               lambda: self._elimina_da_tree(self.ric_tree),
               color="danger").pack(side="left")

        self._mostra_tutte()

    def _cerca(self):
        q = self.ric_var.get().strip()
        if not q:
            self._mostra_tutte()
            return
        risultati = db.cerca_frasi_greco(q)
        self._popola_ric(risultati)
        self.ric_info.config(text=f"{len(risultati)} risultati per «{q}»")

    def _mostra_tutte(self):
        tutte = db.get_frasi_greco()
        self._popola_ric(tutte)
        self.ric_info.config(text=f"Tutte le frasi: {len(tutte)}")

    def _popola_ric(self, rows):
        for r in self.ric_tree.get_children():
            self.ric_tree.delete(r)
        for f in rows:
            t  = f[1][:50] + "…" if len(f[1]) > 50 else f[1]
            tr = (f[2] or "")[:50] + "…" if f[2] and len(f[2]) > 50 else (f[2] or "")
            self.ric_tree.insert("", "end", iid=str(f[0]),
                                 values=(f[0], t, tr, f[4] or "—", f[5] or "—", f[6][:10]))

    # ─────────────────────────────────────────
    # UTILITY
    # ─────────────────────────────────────────

    def _elimina_da_tree(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Attenzione", "Seleziona una frase da eliminare.")
            return
        fid = int(sel[0])
        testo = str(tree.item(sel[0])["values"][1])
        if messagebox.askyesno("Conferma eliminazione",
                               f"Eliminare:\n«{testo}»?"):
            db.elimina_frase_greco(fid)
            tree.delete(sel[0])
            self._refresh_ins_tree()
            self._refresh_cat_tree()
            self.status_cb(f"Eliminata  •  {db.count_frasi_greco()} frasi rimaste")

    def vai_inserisci(self):
        self.nb.select(0)

    def vai_ricerca(self):
        self.nb.select(2)
