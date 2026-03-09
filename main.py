"""
main.py — Punto di ingresso dell'applicazione
Archivio Proverbi Italiani & Frasi Latine
"""

import tkinter as tk
from tkinter import ttk, Menu, messagebox
from datetime import datetime
from csv_import import DialogImportaCSV

import database as db
import ui_utils as ui
from tab_proverbi import PannelloProverbi
from tab_latino import PannelloLatino
from tab_greco import PannelloGreco


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📜 Archivio — Proverbi & Frasi Latine")
        self.geometry("960x780")
        self.minsize(720, 520)
        self.configure(bg=ui.COLORS["bg"])
       
        ui.apply_styles(self)

        self._build_topbar()
        self._build_panels()
        self._build_statusbar()

        self._switch_mode()   # mostra il pannello iniziale
        self._update_status()
        self.update_idletasks()
        self.geometry(f"960x780+{(self.winfo_screenwidth()-960)//2}+{(self.winfo_screenheight()-780)//2}")


    # ─────────────────────────────────────────
    # TOP BAR: menu + combo modalità
    # ─────────────────────────────────────────

    def _build_topbar(self):
        # ── Menu ──────────────────────────────
        menubar = Menu(self,
                       bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                       activebackground=ui.COLORS["bg_selected"],
                       activeforeground=ui.COLORS["fg"],
                       relief="flat")
        self.config(menu=menubar)

        m_file = Menu(menubar, tearoff=0,
                      bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                      activebackground=ui.COLORS["bg_selected"],
                      activeforeground=ui.COLORS["fg"])
        m_file.add_command(label="Nuovo elemento",
                           command=self._nuovo, accelerator="Ctrl+N")
        m_file.add_separator()
        m_file.add_command(label="Esci", command=self.quit)
        menubar.add_cascade(label="File", menu=m_file)

        m_modifica = Menu(menubar, tearoff=0,
                          bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                          activebackground=ui.COLORS["bg_selected"],
                          activeforeground=ui.COLORS["fg"])
        m_modifica.add_command(label="Cerca",
                               command=self._cerca, accelerator="Ctrl+F")
        menubar.add_cascade(label="Modifica", menu=m_modifica)

        m_importa = Menu(menubar, tearoff=0,
                         bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                         activebackground=ui.COLORS["bg_selected"],
                         activeforeground=ui.COLORS["fg"])
        m_importa.add_command(label="🇮🇹  Proverbi Italiani da CSV…",
                              command=self._importa_proverbi)
        m_importa.add_command(label="🏛️  Frasi Latine da CSV…",
                              command=self._importa_latino)
        m_importa.add_command(label="🏺  Frasi Greco Antico da CSV…",
                              command=self._importa_greco)
        menubar.add_cascade(label="Importa da CSV", menu=m_importa)

        m_info = Menu(menubar, tearoff=0,
                      bg=ui.COLORS["bg_card"], fg=ui.COLORS["fg"],
                      activebackground=ui.COLORS["bg_selected"],
                      activeforeground=ui.COLORS["fg"])
        m_info.add_command(label="Informazioni", command=self._mostra_info)
        menubar.add_cascade(label="?", menu=m_info)

        self.bind("<Control-n>", lambda e: self._nuovo())
        self.bind("<Control-f>", lambda e: self._cerca())

        # ── Barra modalità (sotto il menu) ────
        bar = tk.Frame(self, bg=ui.COLORS["bg_bar"], height=48)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="Modalità archivio:",
                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["fg_dim"],
                 font=ui.FONTS["label"]).pack(side="left", padx=(16, 8))

        self.mode_var = tk.StringVar(value="🇮🇹  Proverbi Italiani")
        self.mode_cb = ttk.Combobox(
            bar,
            textvariable=self.mode_var,
            values=["🇮🇹  Proverbi Italiani", "🏛️  Frasi Latine", "🏺  Frasi Greco Antico"],
            state="readonly",
            width=24,
            font=("Segoe UI", 11, "bold")
        )
        self.mode_cb.pack(side="left", ipady=4)
        self.mode_cb.bind("<<ComboboxSelected>>", lambda e: self._switch_mode())

        # Badge contatori
        self.badge_it = tk.Label(bar, text="",
                                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["accent_it"],
                                 font=ui.FONTS["small"])
        self.badge_it.pack(side="left", padx=(20, 4))

        self.badge_la = tk.Label(bar, text="",
                                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["accent_la"],
                                 font=ui.FONTS["small"])
        self.badge_la.pack(side="left", padx=(0, 4))

        self.badge_gr = tk.Label(bar, text="",
                                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["accent_gr"],
                                 font=ui.FONTS["small"])
        self.badge_gr.pack(side="left", padx=(0, 4))

        self._refresh_badges()

    # ─────────────────────────────────────────
    # PANNELLI
    # ─────────────────────────────────────────

    def _build_panels(self):
        self.container = tk.Frame(self, bg=ui.COLORS["bg"])
        self.container.pack(fill="both", expand=True, padx=8, pady=(6, 0))

        self.panel_it = PannelloProverbi(self.container, self._update_status)
        self.panel_la = PannelloLatino(self.container,   self._update_status)
        self.panel_gr = PannelloGreco(self.container, self._update_status)

        # Entrambi occupano lo stesso spazio; ne mostriamo uno alla volta
        self.panel_it.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.panel_la.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.panel_gr.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _switch_mode(self):
        val = self.mode_var.get()
        if "Italiano" in val or "Italiani" in val:
            self.panel_it.lift()
            self.configure(bg=ui.COLORS["bg"])
        elif "Latine" in val or "Latino" in val:
            self.panel_la.lift()
            self.configure(bg=ui.COLORS["bg"])
        else:
            self.panel_gr.lift()
            self.configure(bg=ui.COLORS["bg"])
        self._refresh_badges()
        self._update_status()

    def _is_italiano(self):
        return "Italiani" in self.mode_var.get()

    def _refresh_badges(self):
        self.badge_it.config(text=f"🇮🇹 {db.count_proverbi()} proverbi")
        self.badge_la.config(text=f"  🏛️ {db.count_frasi_latino()} latine")
        self.badge_gr.config(text=f"  🏺 {db.count_frasi_greco()} greche")

    # ─────────────────────────────────────────
    # STATUS BAR
    # ─────────────────────────────────────────

    def _build_statusbar(self):
        bar = tk.Frame(self, bg=ui.COLORS["bg_bar"], height=26)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_var = tk.StringVar()
        tk.Label(bar, textvariable=self.status_var,
                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["fg_dim"],
                 font=ui.FONTS["status"], anchor="w",
                 padx=12).pack(side="left", fill="y")

        tk.Label(bar, text=f"PROVERBI & FRASI v. 1.0.1 - DB: {db.DB_PATH}",
                 bg=ui.COLORS["bg_bar"], fg=ui.COLORS["fg_muted"],
                 font=ui.FONTS["status"], anchor="e",
                 padx=12).pack(side="right", fill="y")

    def _update_status(self, msg=None):
        n_it = db.count_proverbi()
        n_la = db.count_frasi_latino()
        ora  = datetime.now().strftime("%H:%M")
       # base = f"🇮🇹 {n_it} proverbi  •  🏛️ {n_la} frasi latine  •  {ora}"
        base = f"🇮🇹 {db.count_proverbi()} proverbi  •  🏛️ {db.count_frasi_latino()} latine  •  🏺 {db.count_frasi_greco()} greche  •  {ora}"
        self.status_var.set(f"{base}   —   {msg}" if msg else base)
        self._refresh_badges()
        if msg:
            self.after(3500, lambda: self._update_status())

    # ─────────────────────────────────────────
    # AZIONI MENU
    # ─────────────────────────────────────────

    def _nuovo(self):
        if self._is_italiano():
            self.panel_it.vai_inserisci()
        elif "Latine" in self.mode_var.get():
            self.panel_la.vai_inserisci()
        else:
            self.panel_gr.vai_inserisci()

    def _cerca(self):
        if self._is_italiano():
            self.panel_it.vai_ricerca()
        elif "Latine" in self.mode_var.get():
            self.panel_la.vai_ricerca()
        else:
            self.panel_gr.vai_ricerca()
    
    def _importa_proverbi(self):
        def aggiorna():
            self.panel_it.vai_ricerca()
            self.panel_it._refresh_ins_tree()
            self.panel_it._refresh_cat_tree()
            self._update_status("Importazione proverbi completata ✅")
        DialogImportaCSV(self, modalita="proverbi", on_done_cb=aggiorna)

    def _importa_latino(self):
        def aggiorna():
            self.panel_la.vai_ricerca()
            self.panel_la._refresh_ins_tree()
            self.panel_la._refresh_cat_tree()
            self._update_status("Importazione frasi latine completata ✅")
        DialogImportaCSV(self, modalita="latino", on_done_cb=aggiorna)
    
    def _importa_greco(self):
        def aggiorna():
            self.panel_gr.vai_ricerca()
            self.panel_gr._refresh_ins_tree()
            self.panel_gr._refresh_cat_tree()
            self._update_status("Importazione frasi greche completata ✅")
        DialogImportaCSV(self, modalita="greco", on_done_cb=aggiorna)
    

    def _mostra_info(self):
        messagebox.showinfo(
            "Informazioni",
            "📜 Archivio Proverbi & Frasi Latine\n\n"
            "Gestisci proverbi italiani e frasi latine\n"
            "con categorie, ricerca e note.\n\n"
            "• Cambia modalità con la combo in alto\n"
            "• Tasto destro sulle righe: copia o elimina\n"
            "• Ctrl+N  →  nuovo elemento\n"
            "• Ctrl+F  →  ricerca\n\n"
            f"DB: {db.DB_PATH}"
        )


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    db.init_db()   # crea le tabelle se non esistono
    app = App()
    app.mainloop()
