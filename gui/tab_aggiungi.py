# gui/tab_aggiungi.py
import tkinter as tk
from tkinter import ttk, messagebox
import db.proverbi_db as pdb
import db.latino_db as ldb
from gui.base_window import Modalita
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app_proverbi import AppProverbi

class TabAggiungi:
    def __init__(self, parent, app: 'AppProverbi'):
        self.parent = parent
        self.app = app
        self.setup_ui()  #← UN SOLO SETUP!
    
    def setup_ui(self):
        # Crea l'interfaccia unificata"""
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        # === CAMPI COMUNI (sempre visibili) ===
        riga = 0
        
        # Tema
        ttk.Label(self.main_frame, text="Tema:", font=('Arial', 11)).grid(row=riga, column=0, sticky='w', pady=5)
        self.entry_tema = ttk.Entry(self.main_frame, width=30, font=('Arial', 11))
        self.entry_tema.grid(row=riga, column=1, pady=5, padx=10)
        riga += 1
        
        # Testo principale (Proverbio o Frase)
        ttk.Label(self.main_frame, text="Testo:", font=('Arial', 11)).grid(row=riga, column=0, sticky='w', pady=5)
        self.text_testo = tk.Text(self.main_frame, height=5, width=40, font=('Arial', 11))
        self.text_testo.grid(row=riga, column=1, pady=5, padx=10)
        riga += 1
        
        # Traduzione (solo per latino - inizialmente nascosta)
        self.label_traduzione = ttk.Label(self.main_frame, text="Traduzione:", font=('Arial', 11))
        self.label_traduzione.grid(row=riga, column=0, sticky='w', pady=5)
        self.text_traduzione = tk.Text(self.main_frame, height=3, width=40, font=('Arial', 11))
        self.text_traduzione.grid(row=riga, column=1, pady=5, padx=10)
        riga += 1
        
        # Autore
        ttk.Label(self.main_frame, text="Autore (opzionale):", font=('Arial', 11)).grid(row=riga, column=0, sticky='w', pady=5)
        self.entry_autore = ttk.Entry(self.main_frame, width=30, font=('Arial', 11))
        self.entry_autore.grid(row=riga, column=1, pady=5, padx=10)
        riga += 1
        
        # Bottone
        self.btn_aggiungi = ttk.Button(self.main_frame, text="Aggiungi", command=self.aggiungi)
        self.btn_aggiungi.grid(row=riga, column=1, pady=20)
        riga += 1
        
        # Label per messaggi
        self.label_messaggio = ttk.Label(self.main_frame, text="", foreground="green")
        self.label_messaggio.grid(row=riga, column=1)
        
        # Nascondi traduzione inizialmente (modalità PROVERBI)
        self._aggiorna_ui_per_modalita()
    
    def _aggiorna_ui_per_modalita(self):
        # Aggiorna label e placeholder in base alla modalità
        if self.app.modalita == Modalita.PROVERBI:
            # Modalità Italiano
            self.label_traduzione.grid_remove()  # Nasconde traduzione
            self.text_traduzione.grid_remove()
            self.btn_aggiungi.config(text="Aggiungi Proverbio")
            # Aggiorna label testo
            for child in self.main_frame.grid_slaves():
                if int(child.grid_info()["row"]) == 1 and int(child.grid_info()["column"]) == 0:
                    if isinstance(child, ttk.Label):
                        child.config(text="Proverbio:")
                        break
        else:
            # Modalità Latino
            self.label_traduzione.grid()  # Mostra traduzione
            self.text_traduzione.grid()
            self.btn_aggiungi.config(text="Aggiungi Frase Latina")
            # Aggiorna label testo
            for child in self.main_frame.grid_slaves():
                if int(child.grid_info()["row"]) == 1 and int(child.grid_info()["column"]) == 0:
                    if isinstance(child, ttk.Label):
                        child.config(text="Frase (Latino):")
                        break
    
    def aggiungi(self):
        # Aggiunge in base alla modalità corrente"""
        tema = self.entry_tema.get().strip().lower()
        testo = self.text_testo.get(1.0, tk.END).strip()
        autore = self.entry_autore.get().strip() or "Anonimo"
        
        if not tema or not testo:
            self.label_messaggio.config(text="Tema e testo sono obbligatori!", foreground="red")
            return
        
        if self.app.modalita == Modalita.PROVERBI:
            self._aggiungi_proverbio(tema, testo, autore)
        else:
            traduzione = self.text_traduzione.get(1.0, tk.END).strip()
            if not traduzione:
                self.label_messaggio.config(text="Traduzione obbligatoria per le frasi latine!", foreground="red")
                return
            self._aggiungi_frase_latina(tema, testo, traduzione, autore)
    
    def _aggiungi_proverbio(self, tema, proverbio, autore):
        # Aggiunge un proverbio italiano"""
        try:
            id_nuovo = pdb.aggiungi_proverbio_db(tema, proverbio, autore)
            self.label_messaggio.config(
                text=f"Proverbio aggiunto! (ID: {id_nuovo})", 
                foreground="green"
            )
            self._pulisci_campi()
            self.app.ricarica_tabelle()
            
            if messagebox.askyesno("Continua", "Proverbio aggiunto! Vuoi vedere l'elenco aggiornato?"):
                self.app.notebook.select(self.app.frame_tutti)
                
        except Exception as e:
            self.label_messaggio.config(text=f"Errore: {str(e)}", foreground="red")
    
    def _aggiungi_frase_latina(self, tema, frase, traduzione, autore):
        # Aggiunge una frase latina"""
        try:
            id_nuovo =  ldb.aggiungi_frase_latino_db(tema, frase, traduzione, autore)
            self.label_messaggio.config(
                text=f"Frase latina aggiunta! (ID: {id_nuovo})", 
                foreground="green"
            )
            self._pulisci_campi()
            self.app.ricarica_tabelle()
            
            if messagebox.askyesno("Continua", "Frase aggiunta! Vuoi vedere l'elenco aggiornato?"):
                self.app.notebook.select(self.app.frame_latino)
                
        except Exception as e:
            self.label_messaggio.config(text=f"Errore: {str(e)}", foreground="red")
    
    def _pulisci_campi(self):
        """Pulisce tutti i campi"""
        self.entry_tema.delete(0, tk.END)
        self.text_testo.delete(1.0, tk.END)
        self.entry_autore.delete(0, tk.END)
        if hasattr(self, 'text_traduzione'):
            self.text_traduzione.delete(1.0, tk.END)