"""
database.py — Gestione database SQLite
Crea automaticamente tabelle per Proverbi Italiani e Frasi Latine
"""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "archivio.db")

# ─────────────────────────────────────────────
# INIT
# ─────────────────────────────────────────────

def init_db():
    """Crea tutte le tabelle all'avvio se non esistono già."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabella categorie proverbi italiani
    c.execute("""
        CREATE TABLE IF NOT EXISTS categorie (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    # Tabella proverbi italiani
    c.execute("""
        CREATE TABLE IF NOT EXISTS proverbi (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            testo        TEXT NOT NULL UNIQUE,
            significato  TEXT,
            categoria_id INTEGER,
            data_ins     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (categoria_id) REFERENCES categorie(id)
        )
    """)

    # Tabella categorie frasi latine
    c.execute("""
        CREATE TABLE IF NOT EXISTS categorie_latino (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    # Tabella frasi latine
    c.execute("""
        CREATE TABLE IF NOT EXISTS frasi_latino (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            testo        TEXT NOT NULL UNIQUE,
            traduzione   TEXT,
            significato  TEXT,
            autore       TEXT,
            categoria_id INTEGER,
            data_ins     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (categoria_id) REFERENCES categorie_latino(id)
        )
    """)

    # ── Dati di default: categorie italiane ──
    for cat in ["Vita e Saggezza", "Amore e Famiglia", "Lavoro e Fortuna",
                "Natura e Stagioni", "Cibo e Salute", "Amicizia", "Altro"]:
        c.execute("INSERT OR IGNORE INTO categorie (nome) VALUES (?)", (cat,))

    # ── Dati di default: proverbi italiani ──
    proverbi = [
        ("Chi dorme non piglia pesci.", "Chi non si impegna non ottiene risultati.", "Lavoro e Fortuna"),
        ("Tra moglie e marito non mettere il dito.", "Non interferire nelle questioni di coppia.", "Amore e Famiglia"),
        ("Il lupo perde il pelo ma non il vizio.", "Le abitudini profonde non cambiano facilmente.", "Vita e Saggezza"),
        ("Rosso di sera, bel tempo si spera.", "Il tramonto rosso annuncia bel tempo.", "Natura e Stagioni"),
        ("A tavola non si invecchia.", "Il momento del pasto è piacevole e rigenerante.", "Cibo e Salute"),
        ("Chi trova un amico trova un tesoro.", "L'amicizia vera è un bene prezioso.", "Amicizia"),
        ("Meglio tardi che mai.", "È preferibile fare una cosa in ritardo che non farla.", "Vita e Saggezza"),
        ("L'abito non fa il monaco.", "L'apparenza non rivela il vero carattere.", "Vita e Saggezza"),
    ]
    for testo, sig, cat_nome in proverbi:
        c.execute("SELECT id FROM categorie WHERE nome=?", (cat_nome,))
        row = c.fetchone()
        if row:
            c.execute("INSERT OR IGNORE INTO proverbi (testo, significato, categoria_id) VALUES (?,?,?)",
                      (testo, sig, row[0]))

    # ── Dati di default: categorie latine ──
    for cat in ["Filosofia", "Diritto", "Guerra e Politica",
                "Amore", "Vita e Morte", "Scienza e Natura", "Altro"]:
        c.execute("INSERT OR IGNORE INTO categorie_latino (nome) VALUES (?)", (cat,))

    # ── Dati di default: frasi latine ──
    frasi = [
        ("Carpe diem.", "Cogli il giorno.", "Vivi il presente senza rimandare.", "Orazio", "Filosofia"),
        ("Alea iacta est.", "Il dado è tratto.", "Una decisione irrevocabile è stata presa.", "Giulio Cesare", "Guerra e Politica"),
        ("Cogito, ergo sum.", "Penso, dunque sono.", "La prova dell'esistenza attraverso il pensiero.", "Cartesio", "Filosofia"),
        ("Veni, vidi, vici.", "Venni, vidi, vinsi.", "Vittoria rapida e decisiva.", "Giulio Cesare", "Guerra e Politica"),
        ("In vino veritas.", "Nel vino c'è la verità.", "Il vino scioglie la lingua e rivela i pensieri veri.", "Plinio il Vecchio", "Vita e Morte"),
        ("Dum spiro, spero.", "Finché respiro, spero.", "Non bisogna mai perdere la speranza finché si è in vita.", "Cicerone", "Vita e Morte"),
        ("Dura lex, sed lex.", "La legge è dura, ma è legge.", "La legge va rispettata anche quando è severa.", "Anonimo", "Diritto"),
        ("Amor vincit omnia.", "L'amore vince su tutto.", "Il potere dell'amore supera ogni ostacolo.", "Virgilio", "Amore"),
    ]
    for testo, trad, sig, autore, cat_nome in frasi:
        c.execute("SELECT id FROM categorie_latino WHERE nome=?", (cat_nome,))
        row = c.fetchone()
        if row:
            c.execute("""
                INSERT OR IGNORE INTO frasi_latino (testo, traduzione, significato, autore, categoria_id)
                VALUES (?,?,?,?,?)
            """, (testo, trad, sig, autore, row[0]))
    
    # Tabella categorie greco antico
    c.execute("""
        CREATE TABLE IF NOT EXISTS categorie_greco (
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT UNIQUE NOT NULL
        )
    """)

    # Tabella frasi greco antico
    c.execute("""
        CREATE TABLE IF NOT EXISTS frasi_greco (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            testo            TEXT NOT NULL UNIQUE,
            traslitterazione TEXT,
            traduzione   TEXT,
            significato  TEXT,
            autore       TEXT,
            categoria_id INTEGER,
            data_ins     TEXT DEFAULT (datetime('now','localtime')),
            FOREIGN KEY (categoria_id) REFERENCES categorie_greco(id)
        )
    """)

    for cat in ["Filosofia", "Epica e Poesia", "Teatro", "Storia",
                "Politica", "Scienza e Medicina", "Altro"]:
        c.execute("INSERT OR IGNORE INTO categorie_greco (nome) VALUES (?)", (cat,))

    frasi_greco = [
        ("Γνῶθι σεαυτόν", "Gnōthi seautón", "Conosci te stesso.", "Principio fondamentale della filosofia greca: l'autoconoscenza come base della saggezza.", "Solone / Delfi", "Filosofia"),
        ("Μηδὲν ἄγαν", "Mēdén ágan", "Niente di troppo.", "La moderazione come virtù suprema, incisa sul tempio di Apollo a Delfi.", "Anonimo / Delfi", "Filosofia"),
        ("Ἄνθρωπος πολιτικὸν ζῷον", "Ánthropos politikón zōon", "L'uomo è un animale politico.", "L'essere umano realizza la sua natura solo nella comunità politica.", "Aristotele", "Politica"),
        ("Πάντα ῥεῖ", "Pánta rheî", "Tutto scorre.", "La realtà è in continuo mutamento, nulla è permanente.", "Eraclito", "Filosofia"),
        ("Ἓν οἶδα ὅτι οὐδὲν οἶδα", "Hén oîda hóti oudén oîda", "So di non sapere nulla.", "La consapevolezza della propria ignoranza è il primo passo verso la saggezza.", "Socrate", "Filosofia"),
        ("Ζῷον λογικόν", "Zōon logikón", "Animale razionale.", "Definizione dell'essere umano come essere dotato di ragione e linguaggio.", "Aristotele", "Filosofia"),
        ("Κτῆμα ἐς ἀεί", "Ktêma es aeí", "Un possesso per sempre.", "Tucidide definisce così la sua opera storica, scritta per durare nel tempo.", "Tucidide", "Storia"),
        ("Μῆνιν ἄειδε θεά", "Mênin áeide theá", "Canta, o dea, l'ira.", "Verso iniziale dell'Iliade, invocazione alla Musa.", "Omero", "Epica e Poesia"),
    ]
    for testo, trasl, trad, sig, autore, cat_nome in frasi_greco:
        c.execute("SELECT id FROM categorie_greco WHERE nome=?", (cat_nome,))
        row = c.fetchone()
        if row:
            c.execute("""
                INSERT OR IGNORE INTO frasi_greco (testo, traslitterazione, traduzione, significato, autore, categoria_id)
                VALUES (?,?,?,?,?,?)
            """, (testo, trasl, trad, sig, autore, row[0]))

    conn.commit()
    conn.close()


# ─────────────────────────────────────────────
# CONNESSIONE
# ─────────────────────────────────────────────

def get_conn():
    return sqlite3.connect(DB_PATH)


# ─────────────────────────────────────────────
# PROVERBI ITALIANI
# ─────────────────────────────────────────────

def get_categorie():
    with get_conn() as conn:
        return conn.execute("SELECT id, nome FROM categorie ORDER BY nome").fetchall()

def get_proverbi(categoria_id=None):
    with get_conn() as conn:
        if categoria_id:
            return conn.execute("""
                SELECT p.id, p.testo, p.significato, c.nome, p.data_ins
                FROM proverbi p LEFT JOIN categorie c ON p.categoria_id=c.id
                WHERE p.categoria_id=? ORDER BY p.id DESC
            """, (categoria_id,)).fetchall()
        return conn.execute("""
            SELECT p.id, p.testo, p.significato, c.nome, p.data_ins
            FROM proverbi p LEFT JOIN categorie c ON p.categoria_id=c.id
            ORDER BY p.id DESC
        """).fetchall()

def cerca_proverbi(testo):
    with get_conn() as conn:
        q = f"%{testo}%"
        return conn.execute("""
            SELECT p.id, p.testo, p.significato, c.nome, p.data_ins
            FROM proverbi p LEFT JOIN categorie c ON p.categoria_id=c.id
            WHERE p.testo LIKE ? OR p.significato LIKE ?
            ORDER BY p.id DESC
        """, (q, q)).fetchall()

def inserisci_proverbio(testo, significato, categoria_id):
    with get_conn() as conn:
        conn.execute("INSERT INTO proverbi (testo, significato, categoria_id) VALUES (?,?,?)",
                     (testo, significato, categoria_id))
        conn.commit()

def elimina_proverbio(pid):
    with get_conn() as conn:
        conn.execute("DELETE FROM proverbi WHERE id=?", (pid,))
        conn.commit()

def inserisci_categoria(nome):
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO categorie (nome) VALUES (?)", (nome,))
        conn.commit()

def elimina_categoria(cat_id):
    with get_conn() as conn:
        conn.execute("UPDATE proverbi SET categoria_id=NULL WHERE categoria_id=?", (cat_id,))
        conn.execute("DELETE FROM categorie WHERE id=?", (cat_id,))
        conn.commit()

def count_proverbi():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM proverbi").fetchone()[0]

def get_cat_proverbi_stats():
    with get_conn() as conn:
        return conn.execute("""
            SELECT c.id, c.nome, COUNT(p.id)
            FROM categorie c LEFT JOIN proverbi p ON p.categoria_id=c.id
            GROUP BY c.id ORDER BY c.nome
        """).fetchall()


# ─────────────────────────────────────────────
# FRASI LATINE
# ─────────────────────────────────────────────

def get_categorie_latino():
    with get_conn() as conn:
        return conn.execute("SELECT id, nome FROM categorie_latino ORDER BY nome").fetchall()

def get_frasi_latino(categoria_id=None):
    with get_conn() as conn:
        if categoria_id:
            return conn.execute("""
                SELECT f.id, f.testo, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
                FROM frasi_latino f LEFT JOIN categorie_latino c ON f.categoria_id=c.id
                WHERE f.categoria_id=? ORDER BY f.id DESC
            """, (categoria_id,)).fetchall()
        return conn.execute("""
            SELECT f.id, f.testo, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
            FROM frasi_latino f LEFT JOIN categorie_latino c ON f.categoria_id=c.id
            ORDER BY f.id DESC
        """).fetchall()

def cerca_frasi_latino(testo):
    with get_conn() as conn:
        q = f"%{testo}%"
        return conn.execute("""
            SELECT f.id, f.testo, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
            FROM frasi_latino f LEFT JOIN categorie_latino c ON f.categoria_id=c.id
            WHERE f.testo LIKE ? OR f.traduzione LIKE ? OR f.significato LIKE ? OR f.autore LIKE ?
            ORDER BY f.id DESC
        """, (q, q, q, q)).fetchall()

def inserisci_frase_latino(testo, traduzione, significato, autore, categoria_id):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO frasi_latino (testo, traduzione, significato, autore, categoria_id)
            VALUES (?,?,?,?,?)
        """, (testo, traduzione, significato, autore, categoria_id))
        conn.commit()

def elimina_frase_latino(fid):
    with get_conn() as conn:
        conn.execute("DELETE FROM frasi_latino WHERE id=?", (fid,))
        conn.commit()

def inserisci_categoria_latino(nome):
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO categorie_latino (nome) VALUES (?)", (nome,))
        conn.commit()

def elimina_categoria_latino(cat_id):
    with get_conn() as conn:
        conn.execute("UPDATE frasi_latino SET categoria_id=NULL WHERE categoria_id=?", (cat_id,))
        conn.execute("DELETE FROM categorie_latino WHERE id=?", (cat_id,))
        conn.commit()

def count_frasi_latino():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM frasi_latino").fetchone()[0]

def get_cat_latino_stats():
    with get_conn() as conn:
        return conn.execute("""
            SELECT c.id, c.nome, COUNT(f.id)
            FROM categorie_latino c LEFT JOIN frasi_latino f ON f.categoria_id=c.id
            GROUP BY c.id ORDER BY c.nome
        """).fetchall()
# ─────────────────────────────────────────────
# FRASI GRECO ANTICO
# ─────────────────────────────────────────────

def get_categorie_greco():
    with get_conn() as conn:
        return conn.execute("SELECT id, nome FROM categorie_greco ORDER BY nome").fetchall()

def get_frasi_greco(categoria_id=None):
    with get_conn() as conn:
        if categoria_id:
            return conn.execute("""
                SELECT f.id, f.testo, f.traslitterazione, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
                FROM frasi_greco f LEFT JOIN categorie_greco c ON f.categoria_id=c.id
                WHERE f.categoria_id=? ORDER BY f.id DESC
            """, (categoria_id,)).fetchall()
        return conn.execute("""
            SELECT f.id, f.testo, f.traslitterazione, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
            FROM frasi_greco f LEFT JOIN categorie_greco c ON f.categoria_id=c.id
            ORDER BY f.id DESC
        """).fetchall()

def cerca_frasi_greco(testo):
    with get_conn() as conn:
        q = f"%{testo}%"
        return conn.execute("""
            SELECT f.id, f.testo, f.traslitterazione, f.traduzione, f.significato, f.autore, c.nome, f.data_ins
            FROM frasi_greco f LEFT JOIN categorie_greco c ON f.categoria_id=c.id
            WHERE f.testo LIKE ? OR f.traduzione LIKE ? OR f.significato LIKE ? OR f.autore LIKE ? OR f.traslitterazione LIKE ?
            ORDER BY f.id DESC
        """, (q, q, q, q, q)).fetchall()

def inserisci_frase_greco(testo, traslitterazione, traduzione, significato, autore, categoria_id):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO frasi_greco (testo, trasl, sig, autore, cat_id)
            VALUES (?,?,?,?,?,?)
        """, (testo, traslitterazione, traduzione, significato, autore, categoria_id))
        conn.commit()

def elimina_frase_greco(fid):
    with get_conn() as conn:
        conn.execute("DELETE FROM frasi_greco WHERE id=?", (fid,))
        conn.commit()

def inserisci_categoria_greco(nome):
    with get_conn() as conn:
        conn.execute("INSERT OR IGNORE INTO categorie_greco (nome) VALUES (?)", (nome,))
        conn.commit()

def elimina_categoria_greco(cat_id):
    with get_conn() as conn:
        conn.execute("UPDATE frasi_greco SET categoria_id=NULL WHERE categoria_id=?", (cat_id,))
        conn.execute("DELETE FROM categorie_greco WHERE id=?", (cat_id,))
        conn.commit()

def count_frasi_greco():
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM frasi_greco").fetchone()[0]

def get_cat_greco_stats():
    with get_conn() as conn:
        return conn.execute("""
            SELECT c.id, c.nome, COUNT(f.id)
            FROM categorie_greco c LEFT JOIN frasi_greco f ON f.categoria_id=c.id
            GROUP BY c.id ORDER BY c.nome
        """).fetchall()
