"""
csv_import.py — Importazione da file CSV
Gestisce l'importazione di Proverbi Italiani e Frasi Latine
"""

import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import database as db
import ui_utils as ui
from typing import Optional, Callable, Dict, List, Set, Tuple, Any


# ─────────────────────────────────────────────
# COSTANTI
# ─────────────────────────────────────────────

class Modalita:
    """Costanti per le modalità di importazione"""
    PROVERBI = "proverbi"
    LATINO = "latino"
    GRECO = "greco"


# Colonne attese per ogni modalità
COLONNE: Dict[str, List[str]] = {
    Modalita.PROVERBI: ["testo", "significato", "categoria"],
    Modalita.LATINO: ["testo", "traduzione", "significato", "autore", "categoria"],
    Modalita.GRECO: ["testo", "traslitterazione", "traduzione", "significato", "autore", "categoria"],
}

# Intestazioni UI per ogni modalità
INTESTAZIONI: Dict[str, List[str]] = {
    Modalita.PROVERBI: ["Testo", "Significato", "Categoria"],
    Modalita.LATINO: ["Testo", "Traduzione", "Significato", "Autore", "Categoria"],
    Modalita.GRECO: ["Testo", "Traslitterazione", "Traduzione", "Significato", "Autore", "Categoria"],
}

# Larghezze colonne per ogni modalità
LARGHEZZE: Dict[str, List[int]] = {
    Modalita.PROVERBI: [260, 220, 140],
    Modalita.LATINO: [200, 160, 160, 100, 100],
    Modalita.GRECO: [180, 140, 140, 140, 100, 100],
}

# Colori per ogni modalità
COLORE_MODALITA: Dict[str, str] = {
    Modalita.PROVERBI: "green",
    Modalita.LATINO: "yellow",
    Modalita.GRECO: "orange",
}


# ─────────────────────────────────────────────
# DIALOGO IMPORTAZIONE
# ─────────────────────────────────────────────

class DialogImportaCSV(tk.Toplevel):
    """Finestra modale per importare un file CSV."""

    def __init__(self, parent: tk.Widget, modalita: str, on_done_cb: Optional[Callable] = None):
        """
        Args:
            parent: Widget genitore
            modalita: Modalità di importazione ('proverbi', 'latino', 'greco')
            on_done_cb: Callable chiamato dopo importazione riuscita
        """
        super().__init__(parent)
        
        # Validazione modalità
        if modalita not in COLONNE:
            raise ValueError(f"Modalità non valida: {modalita}")
        
        self.parent = parent
        self.modalita = modalita
        self.on_done = on_done_cb
        self.filepath = tk.StringVar()
        self.separatore = tk.StringVar(value=",")
        self.salta_duplicati = tk.BooleanVar(value=True)
        self.righe_anteprima: List[Dict[str, str]] = []
        
        self._setup_finestra()
        self._build_ui()
        self._centra_finestra()

    def _setup_finestra(self):
        """Configura la finestra principale"""
        titoli = {
            Modalita.PROVERBI: "Importa Proverbi Italiani",
            Modalita.LATINO: "Importa Frasi Latine",
            Modalita.GRECO: "Importa Frasi Greche",
        }
        self.title(titoli.get(self.modalita, "Importa CSV"))
        self.geometry("780x660")
        self.minsize(640, 440)
        self.configure(bg=ui.COLORS["bg"])
        self.resizable(True, True)
        self.grab_set()  # Finestra modale
        self.transient(self.parent)

    def _centra_finestra(self):
        """Centra la finestra sullo schermo"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 780) // 2
        y = (self.winfo_screenheight() - 660) // 2
        self.geometry(f"780x660+{x}+{y}")

    def _build_ui(self):
        """Costruisce l'interfaccia utente"""
        main_frame = tk.Frame(self, bg=ui.COLORS["bg"])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self._crea_titolo(main_frame)
        self._crea_selezione_file(main_frame)
        self._crea_opzioni(main_frame)
        self._crea_anteprima(main_frame)
        self._crea_bottoni(main_frame)

    def _crea_titolo(self, parent: tk.Frame):
        """Crea il titolo della finestra"""
        titoli = {
            Modalita.PROVERBI: "📖 Importa Proverbi Italiani",
            Modalita.LATINO: "🏛️ Importa Frasi Latine",
            Modalita.GRECO: "🏺 Importa Frasi Greche",
        }
        titolo = titoli.get(self.modalita, "Importa CSV")
        colore = COLORE_MODALITA.get(self.modalita, "white")
        
        tk.Label(
            parent, 
            text=titolo, 
            bg=ui.COLORS["bg"],
            fg=ui.COLORS[colore] if colore in ui.COLORS else colore,
            font=ui.FONTS["title"]
        ).pack(anchor="w", pady=(0, 2))

        # Informazioni colonne
        colonne = COLONNE[self.modalita]
        tk.Label(
            parent,
            text=f"Colonne richieste: {', '.join(colonne)}  (intestazione obbligatoria)",
            bg=ui.COLORS["bg"],
            fg=ui.COLORS["fg_dim"],
            font=ui.FONTS["small"]
        ).pack(anchor="w", pady=(0, 12))

    def _crea_selezione_file(self, parent: tk.Frame):
        """Crea la sezione di selezione file"""
        frame = tk.Frame(parent, bg=ui.COLORS["bg"])
        frame.pack(fill="x", pady=(0, 10))

        # Entry per il path
        entry = ui.entry_input(frame, textvariable=self.filepath, width=52)
        entry.pack(side="left", ipady=6, padx=(0, 8))

        # Bottone sfoglia
        ui.btn(
            frame, 
            "📂 Sfoglia…", 
            self._sfoglia, 
            color="ghost"
        ).pack(side="left")

    def _crea_opzioni(self, parent: tk.Frame):
        """Crea le opzioni di importazione"""
        frame = tk.Frame(parent, bg=ui.COLORS["bg"])
        frame.pack(fill="x", pady=(0, 10))

        # Separatore
        tk.Label(
            frame,
            text="Separatore:",
            bg=ui.COLORS["bg"],
            fg=ui.COLORS["fg"],
            font=ui.FONTS["label"]
        ).pack(side="left", padx=(0, 8))

        for etichetta, valore in [("Virgola  ,", ","), ("Punto e virgola  ;", ";"), ("Tab  \\t", "\t")]:
            tk.Radiobutton(
                frame,
                text=etichetta,
                variable=self.separatore,
                value=valore,
                bg=ui.COLORS["bg"],
                fg=ui.COLORS["fg"],
                selectcolor=ui.COLORS["bg_card"],
                activebackground=ui.COLORS["bg"],
                font=ui.FONTS["small"]
            ).pack(side="left", padx=(0, 12))

        # Checkbox salta duplicati
        tk.Checkbutton(
            frame,
            text="Salta duplicati (stesso testo già presente)",
            variable=self.salta_duplicati,
            bg=ui.COLORS["bg"],
            fg=ui.COLORS["fg"],
            selectcolor=ui.COLORS["bg_card"],
            activebackground=ui.COLORS["bg"],
            font=ui.FONTS["small"]
        ).pack(side="left", padx=(16, 0))

    def _crea_anteprima(self, parent: tk.Frame):
        """Crea la sezione anteprima"""
        # Label anteprima
        tk.Label(
            parent,
            text="Anteprima (prime 50 righe)",
            bg=ui.COLORS["bg"],
            fg=ui.COLORS["fg_dim"],
            font=ui.FONTS["small"]
        ).pack(anchor="w")

        # Treeview con scroll
        frame_tree, self.tree = ui.scrolled_tree(
            parent,
            columns=INTESTAZIONI[self.modalita],
            headings=INTESTAZIONI[self.modalita],
            widths=LARGHEZZE[self.modalita],
            height=10
        )
        frame_tree.pack(fill="both", expand=True, pady=(4, 5))

        # Label info
        self.info_label = tk.Label(
            parent,
            text="Nessun file selezionato.",
            bg=ui.COLORS["bg"],
            fg=ui.COLORS["fg_dim"],
            font=ui.FONTS["small"],
            anchor="w"
        )
        self.info_label.pack(fill="x", pady=(0, 10))

    def _crea_bottoni(self, parent: tk.Frame):
        """Crea i bottoni di azione"""
        frame = tk.Frame(parent, bg=ui.COLORS["bg"])
        frame.pack(anchor="e")

        # Bottone annulla
        ui.btn(
            frame,
            "Annulla",
            self.destroy,
            color="ghost"
        ).pack(side="left", padx=(0, 8))

        # Bottone importa
        colore = COLORE_MODALITA.get(self.modalita, "green")
        self.btn_importa = ui.btn(
            frame,
            "  ✅  Importa",
            self._importa,
            color=colore
        )
        self.btn_importa.pack(side="left")
        self.btn_importa.config(state="disabled")

    # ── GESTIONE FILE ─────────────────────────

    def _sfoglia(self):
        """Apre il dialog di selezione file"""
        path = filedialog.askopenfilename(
            parent=self,
            title="Seleziona file CSV",
            filetypes=[("File CSV", "*.csv"), ("Tutti i file", "*.*")]
        )
        if path:
            self.filepath.set(path)
            self._carica_anteprima(path)

    def _carica_anteprima(self, path: str):
        """Carica l'anteprima del file CSV"""
        separatore = self.separatore.get()
        colonne_attese = COLONNE[self.modalita]

        # Pulisci treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.righe_anteprima.clear()

        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=separatore)
                headers = [h.strip().lower() for h in (reader.fieldnames or [])]

                # Verifica colonne obbligatorie
                mancanti = [c for c in colonne_attese if c not in headers]
                if mancanti:
                    messagebox.showerror(
                        "Colonne mancanti",
                        f"Il file CSV non contiene le colonne richieste:\n"
                        f"Mancanti: {', '.join(mancanti)}\n\n"
                        f"Presenti: {', '.join(headers)}",
                        parent=self
                    )
                    self.btn_importa.config(state="disabled")
                    self.info_label.config(text="❌ Colonne mancanti — controlla il file.")
                    return

                # Carica anteprima
                for i, row in enumerate(reader):
                    if i >= 50:
                        break
                    
                    # Normalizza chiavi
                    row_normalizzata = {
                        k.strip().lower(): (v or "").strip() 
                        for k, v in row.items()
                    }
                    self.righe_anteprima.append(row_normalizzata)
                    
                    # Prepara valori per visualizzazione
                    valori = tuple(row_normalizzata.get(c, "") for c in colonne_attese)
                    self.tree.insert("", "end", values=valori)

            # Aggiorna info
            n_righe = len(self.righe_anteprima)
            if n_righe > 0:
                self.info_label.config(
                    text=f"✅ {n_righe} righe caricate in anteprima (max 50). Pronto per importare."
                )
                self.btn_importa.config(state="normal")
            else:
                self.info_label.config(text="⚠️ File vuoto o senza dati validi.")
                self.btn_importa.config(state="disabled")

        except Exception as e:
            messagebox.showerror("Errore lettura", str(e), parent=self)
            self.info_label.config(text="❌ Errore nella lettura del file.")
            self.btn_importa.config(state="disabled")

    # ── IMPORTAZIONE ──────────────────────────

    def _importa(self):
        """Esegue l'importazione dei dati dal CSV"""
        path = self.filepath.get().strip()
        if not path:
            return

        separatore = self.separatore.get()
        salta_dup = self.salta_duplicati.get()
        colonne_attese = COLONNE[self.modalita]

        # Recupera testi esistenti per deduplicazione
        testi_esistenti = self._get_testi_esistenti()

        importati = 0
        saltati = 0
        errori = 0

        try:
            with open(path, newline="", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f, delimiter=separatore)
                
                for row in reader:
                    # Normalizza riga
                    riga = {
                        k.strip().lower(): (v or "").strip() 
                        for k, v in row.items()
                    }
                    
                    testo = riga.get("testo", "")
                    if not testo:
                        errori += 1
                        continue

                    # Controllo duplicati
                    if salta_dup and testo.lower() in testi_esistenti:
                        saltati += 1
                        continue

                    try:
                        if self.modalita == Modalita.PROVERBI:
                            self._importa_proverbio(riga)
                        elif self.modalita == Modalita.LATINO:
                            self._importa_latino(riga)
                        elif self.modalita == Modalita.GRECO:
                            self._importa_greco(riga)
                        
                        testi_esistenti.add(testo.lower())
                        importati += 1
                        
                    except Exception:
                        errori += 1

        except Exception as e:
            messagebox.showerror("Errore importazione", str(e), parent=self)
            return

        # Mostra risultato
        self._mostra_risultato(importati, saltati, errori)

    def _get_testi_esistenti(self) -> Set[str]:
        """Recupera i testi già presenti nel database"""
        testi = set()
        
        try:
            if self.modalita == Modalita.PROVERBI:
                for row in db.get_proverbi():
                    if len(row) > 1 and row[1]:
                        testi.add(row[1].strip().lower())
            elif self.modalita == Modalita.LATINO:
                for row in db.get_frasi_latino():
                    if len(row) > 1 and row[1]:
                        testi.add(row[1].strip().lower())
            elif self.modalita == Modalita.GRECO:
                # Aggiungi qui la chiamata per il greco quando disponibile
                pass
        except Exception as e:
            print(f"Errore nel recupero testi esistenti: {e}")
            
        return testi

    def _importa_proverbio(self, riga: Dict[str, str]):
        """Importa un proverbio italiano"""
        testo = riga.get("testo", "")
        significato = riga.get("significato", "")
        categoria_nome = riga.get("categoria", "")
        
        categoria_id = self._get_or_create_categoria(categoria_nome, Modalita.PROVERBI)
        db.inserisci_proverbio(testo, significato, categoria_id)

    def _importa_latino(self, riga: Dict[str, str]):
        """Importa una frase latina"""
        testo = riga.get("testo", "")
        traduzione = riga.get("traduzione", "")
        significato = riga.get("significato", "")
        autore = riga.get("autore", "")
        categoria_nome = riga.get("categoria", "")
        
        categoria_id = self._get_or_create_categoria(categoria_nome, Modalita.LATINO)
        db.inserisci_frase_latino(testo, traduzione, significato, autore, categoria_id)

    def _importa_greco(self, riga: Dict[str, str]):
        """Importa una frase greca"""
        testo = riga.get("testo", "")
        traslitterazione = riga.get("traslitterazione", "")
        traduzione = riga.get("traduzione", "")
        significato = riga.get("significato", "")
        autore = riga.get("autore", "")
        categoria_nome = riga.get("categoria", "")
        
        categoria_id = self._get_or_create_categoria(categoria_nome, Modalita.GRECO)
        # Assumendo che esista una funzione db.inserisci_frase_greco()
        # db.inserisci_frase_greco(testo, traslitterazione, traduzione, significato, autore, categoria_id)

    def _get_or_create_categoria(self, nome: str, tipo: str) -> Optional[int]:
        """
        Restituisce l'ID della categoria, creandola se non esiste.
        
        Args:
            nome: Nome della categoria
            tipo: Tipo di categoria ('proverbi', 'latino', 'greco')
            
        Returns:
            ID della categoria o None se nome vuoto
        """
        if not nome or not nome.strip():
            return None
            
        nome = nome.strip()
        
        try:
            if tipo == Modalita.PROVERBI:
                # Cerca categoria esistente
                for cat_id, cat_nome in db.get_categorie():
                    if cat_nome.lower() == nome.lower():
                        return cat_id
                # Crea nuova categoria
                db.inserisci_categoria(nome)
                for cat_id, cat_nome in db.get_categorie():
                    if cat_nome.lower() == nome.lower():
                        return cat_id
                        
            elif tipo == Modalita.LATINO:
                for cat_id, cat_nome in db.get_categorie_latino():
                    if cat_nome.lower() == nome.lower():
                        return cat_id
                db.inserisci_categoria_latino(nome)
                for cat_id, cat_nome in db.get_categorie_latino():
                    if cat_nome.lower() == nome.lower():
                        return cat_id
                        
            elif tipo == Modalita.GRECO:
                # Aggiungi qui la logica per il greco quando disponibile
                pass
                
        except Exception as e:
            print(f"Errore nella gestione categoria: {e}")
            
        return None

    def _mostra_risultato(self, importati: int, saltati: int, errori: int):
        """Mostra il riepilogo dell'importazione"""
        msg = (
            f"Importazione completata!\n\n"
            f"✅ Importati: {importati}\n"
            f"⏭️  Saltati: {saltati}\n"
            f"❌ Errori: {errori}"
        )
        messagebox.showinfo("Importazione completata", msg, parent=self)

        if self.on_done:
            self.on_done()
            
        self.destroy()