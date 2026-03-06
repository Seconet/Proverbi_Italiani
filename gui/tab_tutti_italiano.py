# Tab tutti proverbi

import sqlite3
import tkinter as tk
from tkinter import ttk
from gui.base_window import Modalita
import db.proverbi_db as pdb
import db.latino_db as ldb


class TabTuttiItaliano:

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app  # Riferimento all'app principale

 
    def setup_tab_tutti(self):
        # Treeview per mostrare tutti i proverbi
        columns = ('ID', 'Tema', 'Proverbio', 'Autore')
        self.tree = ttk.Treeview(self.parent, columns=columns, show='headings', height=20)
        
        # Definizione colonne
        self.tree.heading('ID', text='ID')
        self.tree.heading('Tema', text='Tema')
        self.tree.heading('Proverbio', text='Proverbio')
        self.tree.heading('Autore', text='Autore')
        
        self.tree.column('ID', width=50)
        self.tree.column('Tema', width=100)
        self.tree.column('Proverbio', width=350)
        self.tree.column('Autore', width=150)
        
        scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        scrollbar.pack(side='right', fill='y', pady=10)
        
        # Bottone per ricaricare
        ttk.Button(self.parent, text="↻ Ricarica", command=self.carica_tutti).pack(pady=5)
        
        # Carica dati
        self.carica_tutti()

    def carica_tutti(self):
        # Pulisci tree
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Carica dati dal database
        conn = sqlite3.connect('frasi.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, tema, proverbio, autore FROM proverbi ORDER BY tema, id')
        
        for row in cursor.fetchall():
            self.tree.insert('', 'end', values=row)
        
        conn.close()