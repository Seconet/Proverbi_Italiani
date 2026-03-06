import tkinter as tk
from tkinter import ttk, messagebox
import db.proverbi_db as pdb
import db.latino_db as ldb
from enum import Enum
 # Classe base con funzioni comuni


class Modalita(Enum):
    PROVERBI = "italiano"
    LATINO = "latino"

class BaseWindow:
    # Classe base con funzionalità comuni a tutte le tab 

    def __init__(self, root):
        self.root = root
        self.modalita = Modalita.PROVERBI
        self.notebook = None
        self.frame_ricerca = None
        self.frame_aggiungi = None
        self.frame_tutti = None
        self.frame_latino = None
        
        # Riferimenti ai database
        self.pdb = pdb
        self.ldb = ldb

    def setup_base_ui(self):
    # Setup degli elementi comuni (menu, status bar, ecc.)
    # Frame per la modalità (in alto)
        frame_controlli = ttk.Frame(self.root)
        frame_controlli.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_controlli, text="Modalità:", font=('Arial', 10)).pack(side='left', padx=5)
        
        self.modalita_combo = ttk.Combobox(frame_controlli, 
                                        values=["Italiano (Proverbi)", "Latino (Frasi)"],
                                        state="readonly", width=20)
        self.modalita_combo.pack(side='left', padx=5)
        self.modalita_combo.set("Italiano (Proverbi)")
        self.modalita_combo.bind('<<ComboboxSelected>>', self.cambia_modalita)
        
        self.label_stato = ttk.Label(frame_controlli, text="ITA", font=('Arial', 10, 'bold'))
        self.label_stato.pack(side='left', padx=10)
        
        # Notebook principale
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)



    def cambia_modalita(self, event=None):
        #Cambia la modalità in base alla selezione del combobox"""
        scelta = self.modalita_combo.get()
        
        if scelta == "Italiano (Proverbi)":
            self.modalita = Modalita.PROVERBI
            self.label_stato.config(text="ITALIANO")
            # Cambia il testo della tab di ricerca (indice 0)
            self.notebook.tab(0, text="Cerca Proverbi")
        else:
            self.modalita = Modalita.LATINO
            self.label_stato.config(text="LATINO")
            # Cambia il testo della tab di ricerca (indice 0)
            self.notebook.tab(0, text="Cerca Frasi Latine")
        
         # Aggiorna la visibilità delle tab (se il metodo esiste)
        if hasattr(self, 'aggiorna_visibilita_tab'):
            self.aggiorna_visibilita_tab()  


    def aggiorna_visibilita_tab(self):
        # Mostra/nasconde le tab in base alla modalità corrente"""
        # Ottieni l'elenco delle tab attuali
        tab_count = self.notebook.index('end')
        
        if self.modalita == Modalita.PROVERBI:
            # Modalità Italiano: mostra tab proverbi, nascondi tab latino
            self.notebook.tab(self.frame_tutti, state='normal')  # Mostra
            self.notebook.tab(self.frame_latino, state='hidden')  # Nascondi
            
            # Se la tab nascosta era selezionata, passa alla prima tab
            if self.notebook.index('current') == self.notebook.index(self.frame_latino):
                self.notebook.select(0)
                
        else:
            # Modalità Latino: mostra tab latino, nascondi tab proverbi
            self.notebook.tab(self.frame_tutti, state='hidden')  # Nascondi
            self.notebook.tab(self.frame_latino, state='normal')  # Mostra
            
            # Se la tab nascosta era selezionata, passa alla prima tab
            if self.notebook.index('current') == self.notebook.index(self.frame_tutti):
                self.notebook.select(0)


   