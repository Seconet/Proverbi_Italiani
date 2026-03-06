# Tab tutte frasi latine
import sqlite3
import tkinter as tk
from tkinter import ttk
from gui.base_window import Modalita


class TabTuttiLatino:

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app  # Riferimento all'app principale


    def setup_tab_latino(self):
            # Tab per visualizzare tutte le frasi latine"""
            columns = ('id', 'tema', 'frase', 'traduzione', 'autore')
            self.tree_latino = ttk.Treeview(self.parent, columns=columns, show='headings', height=20)
            
            self.tree_latino.heading('id', text='ID')
            self.tree_latino.heading('tema', text='Tema')
            self.tree_latino.heading('frase', text='Frase (Latino)')
            self.tree_latino.heading('traduzione', text='Traduzione')
            self.tree_latino.heading('autore', text='Autore')
            
            # ... configurazione colonne e scrollbar ...
            # Larghezza colonne (usa gli stessi nomi)
            self.tree_latino.column('id', width=50)
            self.tree_latino.column('tema', width=100)
            self.tree_latino.column('frase', width=250)
            self.tree_latino.column('traduzione', width=200)
            self.tree_latino.column('autore', width=100)

            scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree_latino.yview)
            self.tree_latino.configure(yscrollcommand=scrollbar.set)
            
            self.tree_latino.pack(side='left', fill='both', expand=True, padx=10, pady=10)
            scrollbar.pack(side='right', fill='y', pady=10)
            
            ttk.Button(self.parent, text="↻ Ricarica", command=self.carica_tutti_latino).pack(pady=5)
            self.carica_tutti_latino()


    def carica_tutti_latino(self):
     
         # Pulisci tree
        for row in self.tree_latino.get_children():
            self.tree_latino.delete(row)
        
        # Carica dati dal database
        conn = sqlite3.connect('frasi.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, tema, frase, traduzione, autore FROM frasi_latine ORDER BY tema, id')
        
        for row in cursor.fetchall():
            self.tree_latino.insert('', 'end', values=row)
        
        conn.close()