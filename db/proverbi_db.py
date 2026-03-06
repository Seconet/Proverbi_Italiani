import sqlite3
import os
import sys

# DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'frasi.db')

def get_db_path():
    # Restituisce il path corretto del database"""
    if getattr(sys, 'frozen', False):
        # Siamo in eseguibile - salva nella cartella dell'exe
        return os.path.join(os.path.dirname(sys.executable), 'frasi.db')
    else:
        # Siamo in sviluppo - salva nella cartella principale
        return os.path.join(os.path.dirname(__file__), '..', 'frasi.db')


# --- GESTIONE DATABASE ---
def crea_tabella_proverbi():
    # Crea il database e la tabella se non esistono
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Crea tabella proverbi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS proverbi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema TEXT NOT NULL,
            proverbio TEXT NOT NULL,
            autore TEXT DEFAULT 'Anonimo',
            data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserisci alcuni proverbi di esempio se la tabella è vuota
    cursor.execute('SELECT COUNT(*) FROM proverbi')
    if cursor.fetchone()[0] == 0:
        proverbi_iniziali = [
            ('amore', 'L\'amore non è bello se non è litigarello', 'Saggezza popolare'),
            ('amore', 'Amore e gelosia nacquero insieme', 'Proverbio italiano'),
            ('amore', 'Lontano dagli occhi, lontano dal cuore', 'Proverbio toscano'),
            ('amore', 'Al cuor non si comanda', 'Proverbio'),
            ('amore', 'Amor con amor si paga', 'Proverbio'),
            ('amore', 'Chi ama teme', 'Proverbio'),
            ('amore', 'Amore cieco, ma vede lontano', 'Proverbio'),
            ('amore', 'Amore fa passare il tempo e il tempo fa passare l\'amore', 'Proverbio'),
            ('lavoro', 'Chi ben comincia è a metà dell\'opera', 'Orazio'),
            ('lavoro', 'Il lavoro nobilita l\'uomo', 'Proverbio'),
            ('lavoro', 'Non rimandare a domani quello che puoi fare oggi', 'Benjamin Franklin'),
            ('lavoro', 'Chi dorme non piglia pesci', 'Proverbio'),
            ('lavoro', 'Chi non lavora non mangia', 'Proverbio'),
            ('lavoro', 'A lavoro fatto, ognuno è maestro', 'Proverbio'),
            ('lavoro', 'L\'ozio è il padre dei vizi', 'Proverbio'),
            ('lavoro', 'Meglio fare che promettere', 'Proverbio'),
            ('tempo', 'Il tempo è denaro', 'Benjamin Franklin'),
            ('tempo', 'Chi tempo ha e tempo aspetta, tempo perde', 'Proverbio'),
            ('tempo', 'Il mattino ha l\'oro in bocca', 'Proverbio'),
            ('tempo', 'Il tempo sistema ogni cosa', 'Proverbio'),
            ('tempo', 'C\'è un tempo per ogni cosa', 'Proverbio'),
            ('tempo', 'Il tempo vola', 'Proverbio'),
            ('tempo', 'Col tempo e con la paglia maturano le nespole', 'Proverbio'),
            ('tempo', 'Il tempo guarisce tutte le ferite', 'Proverbio'),
            ('amicizia', 'Chi trova un amico trova un tesoro', 'Proverbio'),
            ('amicizia', 'L\'amico si vede nel bisogno', 'Proverbio latino'),
            ('amicizia', 'Dimmi con chi vai e ti dirò chi sei', 'Proverbio'),
            ('amicizia', 'Amici pochi ma buoni', 'Proverbio'),
            ('amicizia', 'Chi trova un amico trova conforto', 'Proverbio'),
            ('amicizia', 'Gli amici si riconoscono nel momento del bisogno', 'Proverbio'),
            ('amicizia', 'Meglio un amico vicino che un parente lontano', 'Proverbio'),
            ('amicizia', 'Chi ha cento amici non ne ha uno', 'Proverbio orientale'),
            ('vita', 'Finché c\'è vita c\'è speranza', 'Proverbio'),
            ('vita', 'La vita è come un\'ombra che passa', 'Salmo 144'),
            ('vita', 'Carpe Diem', 'Orazio'),
            ('vita', 'La vita è una ruota che gira', 'Proverbio'),
            ('vita', 'Chi vive sperando muore cantando', 'Proverbio'),
            ('vita', 'La vita insegna più dei libri', 'Proverbio'),
            ('vita', 'La vita è breve ma larga', 'Proverbio'),
            ('vita', 'Vivi e lascia vivere', 'Proverbio'),
            ('saggezza', 'Chi sa tace', 'Proverbio'),
            ('saggezza', 'Meglio tardi che mai', 'Proverbio'),
            ('saggezza', 'Chi cerca trova', 'Proverbio'),
            ('saggezza', 'Chi troppo vuole nulla stringe', 'Proverbio'),
            ('saggezza', 'Impara l\'arte e mettila da parte', 'Proverbio'),
            ('fortuna', 'La fortuna aiuta gli audaci', 'Proverbio'),
            ('fortuna', 'La fortuna è cieca ma la sfortuna ci vede benissimo', 'Proverbio'),
            ('fortuna', 'Chi ha fortuna non si lamenti', 'Proverbio'),
            ('fortuna', 'La fortuna gira', 'Proverbio'),
            ('fortuna', 'La fortuna bacia i coraggiosi', 'Proverbio'),
            ('destino', 'Ognuno è artefice del proprio destino', 'Proverbio'),
            ('destino', 'Quel che deve accadere accadrà', 'Proverbio'),
            ('destino', 'Il destino mescola le carte e noi giochiamo', 'Proverbio'),
            ('destino', 'Il destino aiuta chi osa', 'Proverbio'),
            ('destino', 'Ciò che è scritto accade', 'Proverbio'),
            ('famiglia', 'Buon sangue non mente', 'Proverbio'),
            ('famiglia', 'Di padre in figlio', 'Proverbio'),
            ('famiglia', 'Tale padre tale figlio', 'Proverbio'),
            ('prudenza', 'Fidarsi è bene, non fidarsi è meglio', 'Proverbio'),
            ('prudenza', 'Chi va piano va sano e va lontano', 'Proverbio'),
            ('prudenza', 'Prevenire è meglio che curare', 'Proverbio'),
            ('verità', 'La verità viene sempre a galla', 'Proverbio'),
            ('verità', 'La verità fa male ma guarisce', 'Proverbio'),
            ('verità', 'Il tempo rivela la verità', 'Proverbio'),
            ('verità', 'La verità trionfa sempre', 'Proverbio')
        ]















        
        cursor.executemany(
            'INSERT INTO proverbi (tema, proverbio, autore) VALUES (?, ?, ?)',
            proverbi_iniziali
        )
    
    conn.commit()
    conn.close()

def cerca_proverbi_db(tema):
    # Cerca proverbi per tema nel database
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    # Cerca proverbi che contengono il tema (ricerca fuzzy)
    cursor.execute('''
        SELECT proverbio, autore FROM proverbi 
        WHERE tema LIKE ? OR proverbio LIKE ?
        ORDER BY RANDOM()
    ''', (f'%{tema}%', f'%{tema}%'))
    
    risultati = cursor.fetchall()
    conn.close()
    
    return risultati

def tutti_temi():
    # Restituisce tutti i temi disponibili
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT tema FROM proverbi ORDER BY tema')
    temi = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return temi

def aggiungi_proverbio_db(tema, proverbio, autore="Anonimo"):
    # Aggiunge un nuovo proverbio al database
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO proverbi (tema, proverbio, autore)
        VALUES (?, ?, ?)
    ''', (tema.lower(), proverbio, autore))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid


