# Tab ricerca (italiano/latino)--> gui/tab_ricerca.py
import tkinter as tk
from tkinter import ttk, messagebox
from gui.base_window import Modalita
import db.proverbi_db as pdb
import db.latino_db as ldb

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app_proverbi import AppProverbi # ← Solo per l'IDE

class TabRicerca:

    def __init__(self, parent, app: 'AppProverbi'):
        self.parent = parent
        self.app = app  # Riferimento all'app principale
        self.modalita = Modalita.PROVERBI
     

    def setup_tab_ricerca(self):
        # Frame per input
        frame_input = ttk.Frame(self.parent)
        frame_input.pack(pady=20)
        
        ttk.Label(frame_input, text="Inserisci tema o parola chiave:", 
                 font=('Arial', 12)).pack(side='left', padx=5)
        
        self.entry_ricerca = ttk.Entry(frame_input, width=30, font=('Arial', 11))
        self.entry_ricerca.pack(side='left', padx=5)
        self.entry_ricerca.bind('<Return>', lambda e: self.cerca())

        # Placeholder iniziale
        if self.modalita == Modalita.PROVERBI:
            self.entry_ricerca.insert(0, "es. amore, lavoro, tempo...")
        else:
            self.entry_ricerca.insert(0, "es. amor, tempus, vita...")
        
        ttk.Button(frame_input, text="Cerca", command=self.cerca).pack(side='left', padx=5)
        
        # Lista temi suggeriti
        frame_suggeriti = ttk.Frame(self.parent)
        frame_suggeriti.pack(pady=10)
        
        ttk.Label(frame_suggeriti, text="Temi suggeriti:").pack()
  
        # Frame per i bottoni dei temi suggeriti (lo teniamo come attributo)
        self.frame_suggeriti = ttk.Frame(self.parent)
        self.frame_suggeriti.pack(pady=10)

        self.frame_bottoni = ttk.Frame(self.frame_suggeriti)
        self.frame_bottoni.pack()
        self.aggiorna_suggerimenti()
        
        # Area risultati
        self.text_risultati = tk.Text(self.parent, height=20, width=80, 
                                     font=('Arial', 10), wrap='word')
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', 
                                 command=self.text_risultati.yview)
        self.text_risultati.configure(yscrollcommand=scrollbar.set)
        
        self.text_risultati.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)



    def cerca(self):
        tema = self.entry_ricerca.get().strip().lower()
        
        # Rimuovi il placeholder se presente
        if tema in ["es. amore, lavoro, tempo", "es. amor, tempus, vita"]:
            tema = ""
        
        if not tema:
            messagebox.showwarning("Attenzione", "Inserisci un tema da cercare!")
            return
        
        self.text_risultati.delete(1.0, tk.END)
        
        if self.app.modalita == Modalita.PROVERBI:
            # Cerca in italiano
            risultati = pdb.cerca_proverbi_db(tema)  # ← usa pdb
            
            if risultati:
                self.text_risultati.insert(tk.END, f"Proverbi trovati per '{tema}':\n\n")
                for i, (proverbio, autore) in enumerate(risultati, 1):
                    self.text_risultati.insert(tk.END, f"{i}. \"{proverbio}\"\n")
                    self.text_risultati.insert(tk.END, f"   └ {autore}\n\n")
            else:
                self.text_risultati.insert(tk.END, f"Nessun proverbio trovato per '{tema}'.")
                temi = pdb.tutti_temi()  # ← usa pdb
                if temi:
                    self.text_risultati.insert(tk.END, f"\nTemi disponibili: {', '.join(temi)}")
        
        else:  # Modalità latino
            # Cerca in latino
            risultati = ldb.cerca_frasi_latine(tema)  # ← usa ldb
            
            if risultati:
                self.text_risultati.insert(tk.END, f"Frasi latine trovate per '{tema}':\n\n")
                for i, (frase, traduzione, autore) in enumerate(risultati, 1):
                    self.text_risultati.insert(tk.END, f"{i}. \"{frase}\"\n")
                    if traduzione:
                        self.text_risultati.insert(tk.END, f"   └ {traduzione}\n")
                    self.text_risultati.insert(tk.END, f"   └ {autore}\n\n")
            else:
                self.text_risultati.insert(tk.END, f"Nessuna frase latina trovata per '{tema}'.")
                temi = ldb.tutti_temi_latini()  # ← supponendo che esista
                if temi:
                    self.text_risultati.insert(tk.END, f"\nTemi disponibili: {', '.join(temi)}")


    def usa_tema(self, tema):
        self.entry_ricerca.delete(0, tk.END)
        self.entry_ricerca.insert(0, tema)
        self.cerca()

    def pulisci_risultati(self):
        # Pulisce l'area dei risultati
        if hasattr(self, 'text_risultati'):
            self.text_risultati.delete(1.0, tk.END)
    
    def aggiorna_placeholder(self, modalita):
        # Aggiorna il placeholder in base alla modalità"""
        self.entry_ricerca.delete(0, tk.END)
        if modalita == Modalita.PROVERBI:
            self.entry_ricerca.insert(0, "es. amore, lavoro, tempo...")
        else:
            self.entry_ricerca.insert(0, "es. amor, tempus, vita...")

        self.aggiorna_suggerimenti() 

    def aggiorna_suggerimenti(self):
        # Aggiorna i bottoni dei temi suggeriti in base alla modalità"""
        # Pulisci i bottoni esistenti
        for widget in self.frame_bottoni.winfo_children():
            widget.destroy()
        
        # Prendi i temi dal database corretto
        if self.app.modalita == Modalita.PROVERBI:
            temi = self.app.pdb.tutti_temi()
        else:
            temi = self.app.ldb.tutti_temi_latino()
        
        # Crea nuovi bottoni
        for tema in temi[:10]:  # Primi 10 temi
            btn = ttk.Button(self.frame_bottoni, text=tema, 
                            command=lambda t=tema: self.usa_tema(t))
            btn.pack(side='left', padx=2)

           