"""
tab_proverbi.py — Pannello completo per i Proverbi Italiani
Contiene i tre tab: Inserisci, Categorie, Ricerca
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database as db
import ui_utils as ui
import sqlite3

import re
from collections import Counter
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches


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
        self.tab_ana  = tk.Frame(self.nb, bg=ui.COLORS["bg"])

        self.nb.add(self.tab_ins, text="  ✏️  Inserisci  ")
        self.nb.add(self.tab_cat, text="  📂  Categorie  ")
        self.nb.add(self.tab_ric, text="  🔍  Ricerca  ")
        self.nb.add(self.tab_ana, text="  🔬  Analisi  ")

        self._build_inserisci()
        self._build_categorie()
        self._build_ricerca()
        self._build_analisi()
    
    
    # ─────────────────────────────────────────
    # TAB ANALISI
    # ─────────────────────────────────────────

    def _build_analisi(self):
        f = self.tab_ana
        ui.section_title(f, "Analisi & Statistiche Proverbi Italiani", "purple")

        top = tk.Frame(f, bg=ui.COLORS["bg"])
        top.pack(fill="x", padx=20, pady=(8, 4))
        ui.btn(top, "  🔄  Aggiorna", self._aggiorna_analisi, color="purple").pack(side="left")
        self.ana_info = tk.Label(top, text="",
                                 bg=ui.COLORS["bg"], fg=ui.COLORS["fg_dim"],
                                 font=ui.FONTS["small"])
        self.ana_info.pack(side="left", padx=16)

        # Scroll container
        outer = tk.Canvas(f, bg=ui.COLORS["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(f, orient="vertical", command=outer.yview)
        outer.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        outer.pack(fill="both", expand=True, padx=(20, 0), pady=(0, 10))

        self.ana_frame = tk.Frame(outer, bg=ui.COLORS["bg"])
        self._ana_win_id = outer.create_window((0, 0), window=self.ana_frame, anchor="nw")

        outer.bind("<Configure>",
                   lambda e: outer.itemconfig(self._ana_win_id, width=e.width))
        self.ana_frame.bind("<Configure>",
                            lambda e: outer.configure(scrollregion=outer.bbox("all")))
        outer.bind("<MouseWheel>",
                   lambda e: outer.yview_scroll(-1 * (e.delta // 120), "units"))

        self._aggiorna_analisi()

    def _aggiorna_analisi(self):
        for w in self.ana_frame.winfo_children():
            w.destroy()

        proverbi = db.get_proverbi()
        if not proverbi:
            tk.Label(self.ana_frame, text="Nessun proverbio presente.",
                     bg=ui.COLORS["bg"], fg=ui.COLORS["fg_dim"],
                     font=ui.FONTS["body"]).pack(padx=20, pady=40)
            return

        self.ana_info.config(text=f"Basato su {len(proverbi)} proverbi")

        STOPWORDS = {
            "il","lo","la","i","gli","le","un","uno","una","di","a","da","in",
            "con","su","per","tra","fra","e","o","ma","se","che","chi","non",
            "è","si","ci","vi","ne","del","della","dello","dei","degli","delle",
            "al","alla","allo","ai","agli","alle","dal","dalla","nel","nella",
            "col","sui","sul","sulla","sulle","come","più","mai","però","anche",
            "tutto","tutti","tutte","c'è","c'","l'","d'","s'","n'","m'"
        }

        # Dati
        lunghezze  = [len(p[1]) for p in proverbi]
        parole_tot = sum(len(p[1].split()) for p in proverbi)
        con_sig    = sum(1 for p in proverbi if p[2])
        cats       = db.get_cat_proverbi_stats()
        n_cat_use  = sum(1 for c in cats if c[2] > 0)
        cat_data   = sorted([(c[1], c[2]) for c in cats if c[2] > 0],
                            key=lambda x: x[1], reverse=True)

        tutti_testi   = " ".join(p[1].lower() for p in proverbi)
        parole        = re.findall(r"[a-zàèéìòù']{3,}", tutti_testi)
        parole_fil    = [w for w in parole if w not in STOPWORDS]
        freq          = Counter(parole_fil).most_common(12)

        unici      = list({p[0]: p for p in proverbi}.values())
        piu_lunghi = sorted(unici, key=lambda p: len(p[1]), reverse=True)[:5]
        piu_corti  = sorted(unici, key=lambda p: len(p[1]))[:5]

        # ── KPI ───────────────────────────────────────────────────────────
        self._ana_section("📊 Riepilogo generale")
        kpi = [
            ("Totale proverbi",     str(len(proverbi))),
            ("Categorie usate",     f"{n_cat_use} / {len(cats)}"),
            ("Parole totali",       str(parole_tot)),
            ("Con spiegazione",     f"{con_sig} ({100*con_sig//len(proverbi)}%)"),
            ("Lunghezza media",     f"{sum(lunghezze)//len(lunghezze)} car."),
            ("Proverbio più lungo", f"{max(lunghezze)} car."),
        ]
        self._ana_kpi_grid(kpi)

        # ── GRAFICO 1: Categorie ──────────────────────────────────────────
        self._ana_section("📂 Distribuzione per categoria")
        if cat_data:
            nomi  = [x[0] for x in cat_data]
            valori = [x[1] for x in cat_data]
            palette = plt.cm.get_cmap("coolwarm", len(nomi))
            colors  = [palette(i) for i in range(len(nomi))]

            fig, ax = plt.subplots(figsize=(8, max(2.5, len(nomi) * 0.55)))
            fig.patch.set_facecolor("#2A2A3E")
            ax.set_facecolor("#2A2A3E")
            bars = ax.barh(nomi, valori, color=colors, height=0.6)
            ax.bar_label(bars, fmt="%d", padding=4,
                         color="#CDD6F4", fontsize=9)
            ax.set_xlabel("Numero proverbi", color="#6C7086", fontsize=9)
            ax.tick_params(colors="#CDD6F4", labelsize=9)
            ax.spines[:].set_color("#45475A")
            ax.xaxis.label.set_color("#6C7086")
            for spine in ax.spines.values():
                spine.set_edgecolor("#45475A")
            ax.invert_yaxis()
            fig.tight_layout()
            self._embed_figure(fig)

        # ── GRAFICO 2: Word frequency ─────────────────────────────────────
        self._ana_section("🔤 Parole più frequenti")
        if freq:
            parole_l = [x[0] for x in freq]
            conti    = [x[1] for x in freq]
            cmap     = plt.cm.get_cmap("viridis", len(parole_l))
            colors2  = [cmap(i) for i in range(len(parole_l))]

            fig2, ax2 = plt.subplots(figsize=(8, max(2.5, len(parole_l) * 0.45)))
            fig2.patch.set_facecolor("#2A2A3E")
            ax2.set_facecolor("#2A2A3E")
            bars2 = ax2.barh(parole_l, conti, color=colors2, height=0.6)
            ax2.bar_label(bars2, fmt="%d", padding=4,
                          color="#CDD6F4", fontsize=9)
            ax2.tick_params(colors="#CDD6F4", labelsize=9)
            for spine in ax2.spines.values():
                spine.set_edgecolor("#45475A")
            ax2.invert_yaxis()
            fig2.tight_layout()
            self._embed_figure(fig2)

        # ── GRAFICO 3: Distribuzione lunghezze ────────────────────────────
        self._ana_section("📏 Distribuzione lunghezza proverbi")
        fig3, ax3 = plt.subplots(figsize=(8, 3))
        fig3.patch.set_facecolor("#2A2A3E")
        ax3.set_facecolor("#2A2A3E")
        ax3.hist(lunghezze, bins=min(15, len(set(lunghezze))),
                 color="#CBA6F7", edgecolor="#1E1E2E", linewidth=0.6)
        ax3.set_xlabel("Lunghezza in caratteri", color="#6C7086", fontsize=9)
        ax3.set_ylabel("Numero proverbi",        color="#6C7086", fontsize=9)
        ax3.tick_params(colors="#CDD6F4", labelsize=9)
        for spine in ax3.spines.values():
            spine.set_edgecolor("#45475A")
        # linea media
        media = sum(lunghezze) / len(lunghezze)
        ax3.axvline(media, color="#F9E2AF", linestyle="--", linewidth=1.2,
                    label=f"Media: {media:.0f} car.")
        ax3.legend(facecolor="#313244", edgecolor="#45475A",
                   labelcolor="#CDD6F4", fontsize=9)
        fig3.tight_layout()
        self._embed_figure(fig3)

        # ── LISTA: più lunghi / più corti ─────────────────────────────────
        self._ana_section("📏 Proverbi più lunghi")
        self._ana_lista_proverbi(piu_lunghi)
        self._ana_section("🤏 Proverbi più corti")
        self._ana_lista_proverbi(piu_corti)

    # ── HELPER ────────────────────────────────────────────────────────────

    def _embed_figure(self, fig):
        """Incorpora una figura matplotlib nel frame di analisi."""
        canvas = FigureCanvasTkAgg(fig, master=self.ana_frame)
        canvas.draw()
        widget = canvas.get_tk_widget()
        widget.configure(bg=ui.COLORS["bg_card"],
                         highlightthickness=1,
                         highlightbackground=ui.COLORS["border"])
        widget.pack(fill="x", padx=4, pady=(0, 8))
        plt.close(fig)

    def _ana_section(self, titolo):
        f = tk.Frame(self.ana_frame, bg=ui.COLORS["bg"])
        f.pack(fill="x", padx=4, pady=(18, 6))
        tk.Label(f, text=titolo, bg=ui.COLORS["bg"],
                 fg=ui.COLORS["purple"], font=ui.FONTS["title"]).pack(anchor="w")
        tk.Frame(f, bg=ui.COLORS["border"], height=1).pack(fill="x", pady=(4, 0))

    def _ana_kpi_grid(self, kpi_list):
        grid = tk.Frame(self.ana_frame, bg=ui.COLORS["bg"])
        grid.pack(fill="x", padx=4, pady=(0, 8))
        for i, (label, value) in enumerate(kpi_list):
            card = tk.Frame(grid, bg=ui.COLORS["bg_card"],
                            highlightthickness=1,
                            highlightbackground=ui.COLORS["border"])
            card.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="nsew")
            grid.columnconfigure(i % 3, weight=1)
            tk.Label(card, text=value, bg=ui.COLORS["bg_card"],
                     fg=ui.COLORS["purple"],
                     font=("Segoe UI", 18, "bold")).pack(pady=(14, 2))
            tk.Label(card, text=label, bg=ui.COLORS["bg_card"],
                     fg=ui.COLORS["fg_dim"],
                     font=ui.FONTS["small"]).pack(pady=(0, 14))

    def _ana_lista_proverbi(self, proverbi):
        frame = tk.Frame(self.ana_frame, bg=ui.COLORS["bg_card"],
                         highlightthickness=1,
                         highlightbackground=ui.COLORS["border"])
        frame.pack(fill="x", padx=4, pady=(0, 4))
        for p in proverbi:
            row = tk.Frame(frame, bg=ui.COLORS["bg_card"])
            row.pack(fill="x", padx=12, pady=5)
            tk.Label(row, text=f"{len(p[1])} car.",
                     bg=ui.COLORS["bg_card"], fg=ui.COLORS["teal"],
                     font=("Segoe UI", 9, "bold"), width=8, anchor="w").pack(side="left")
            tk.Label(row,
                     text=p[1][:85] + ("…" if len(p[1]) > 85 else ""),
                     bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                     font=ui.FONTS["small"], anchor="w").pack(side="left", fill="x", expand=True)
            tk.Label(row, text=p[3] or "—",
                     bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg_dim"],
                     font=ui.FONTS["small"], anchor="e").pack(side="right")

   



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
