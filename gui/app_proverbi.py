from gui.base_window import BaseWindow, Modalita
from .tab_ricerca import TabRicerca
from .tab_aggiungi import TabAggiungi
from .tab_tutti_italiano import TabTuttiItaliano 
from .tab_tutti_latino import TabTuttiLatino 
import tkinter as tk
from tkinter import ttk
# Classe principale che unisce tutto

class AppProverbi(BaseWindow):

   def __init__(self, root):
      super().__init__(root)  # Chiama il costruttore della base
      self.root.title("Raccolta Proverbi Italiani e Frasi Latine")
      self.root.geometry("1200x800")
      
      # Crea database
      self.pdb.crea_tabella_proverbi()
      self.ldb.crea_tabella_latino()
      
      # Setup UI base
      self.setup_base_ui()
      
      
      # Crea le tab
      self.crea_tab()
      
      
      # Inizializza
      self.aggiorna_visibilita_tab()
    
   def crea_tab(self):
      # === TAB RICERCA ===
      self.frame_ricerca = ttk.Frame(self.notebook)
      self.notebook.add(self.frame_ricerca, text="Cerca Proverbi")
      self.tab_ricerca = TabRicerca(self.frame_ricerca, self)  
      self.tab_ricerca.setup_tab_ricerca()

      # == TAB TUTTI ITALIANO ===
      self.frame_tutti = ttk.Frame(self.notebook)
      self.notebook.add(self.frame_tutti, text="Tutti i proverbi")
      self.tab_tutti = TabTuttiItaliano(self.frame_tutti, self)
      self.tab_tutti.setup_tab_tutti()

      # == TAB TUTTI LATINO ===
      self.frame_latino = ttk.Frame(self.notebook)
      self.notebook.add(self.frame_latino, text="Tutte le frasi in latino")
      self.tab_tutti_latino = TabTuttiLatino(self.frame_latino,self)
      self.tab_tutti_latino.setup_tab_latino()

      # == TAB AGGIUNGI ===
      self.frame_aggiungi = ttk.Frame(self.notebook)
      self.notebook.add(self.frame_aggiungi, text="Aggiungi")
      self.tab_aggiungi = TabAggiungi(self.frame_aggiungi,self)
      # self.tab_aggiungi.aggiungi()


   def cambia_modalita(self, event=None):
      # Chiama il metodo della classe base
      super().cambia_modalita(event)

      # Aggiorna la visibilità delle tab
      self.aggiorna_visibilita_tab()
      
      # AGGIUNGI QUI - Aggiorna il placeholder nella tab ricerca
      if hasattr(self, 'tab_ricerca'):
         self.tab_ricerca.aggiorna_placeholder(self.modalita)
         self.tab_ricerca.pulisci_risultati()  # Nuovo metodo da aggiungere

      #  Aggiorna la UI della tab aggiungi
      if hasattr(self, 'tab_aggiungi'):
         self.tab_aggiungi._aggiorna_ui_per_modalita()





   def ricarica_tabelle(self):
        # Ricarica entrambe le tabelle
        if hasattr(self, 'tab_tutti'):
            self.tab_tutti.carica_tutti()
        if hasattr(self, 'tab_latino'):
            self.tab_tutti_latino.carica_tutti_latino()




