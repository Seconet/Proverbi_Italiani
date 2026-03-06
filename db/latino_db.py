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


def crea_tabella_latino():
    # Crea la tabella per le frasi latine se non esiste"""
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frasi_latine (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tema TEXT NOT NULL,
            frase TEXT NOT NULL,
            traduzione TEXT,
            autore TEXT DEFAULT 'Anonimo',
            data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Inserisci qualche frase latina se la tabella è vuota
    cursor.execute('SELECT COUNT(*) FROM frasi_latine')
    if cursor.fetchone()[0] == 0:
        frasi_iniziali = [
            ('amore', 'Amor vincit omnia', 'L\'amore vince tutto', 'Virgilio'),
            ('amore', 'Odi et amo', 'Odio e amo', 'Catullo'),
            ('amore', 'Ama et fac quod vis', 'Ama e fai ciò che vuoi', 'Agostino'),
            ('amore', 'Ubi amor, ibi dolor', 'Dove c\'è amore, c\'è dolore', ''),
            ('amore', 'Amor est vitae essentia', 'L\'amore è l\'essenza della vita', ''),
            ('amore', 'Si vis amari, ama', 'Se vuoi essere amato, ama', 'Seneca'),
            ('amore', 'Amantium irae amoris integratio est', 'I litigi degli amanti rafforzano l\'amore', 'Terenzio'),
            ('fortuna', 'Fortuna audaces iuvat', 'La fortuna aiuta gli audaci', 'Virgilio'),
            ('fortuna', 'Audentes fortuna iuvat', 'La fortuna favorisce gli audaci', 'Virgilio'),
            ('fortuna', 'Fortuna caeca est', 'La fortuna è cieca', ''),
            ('fortuna', 'Fortes fortuna adiuvat', 'La fortuna aiuta i forti', ''),
            ('lavoro', 'Labor omnia vincit', 'Il lavoro vince tutto', 'Virgilio'),
            ('lavoro', 'Nulla dies sine linea', 'Nessun giorno senza una riga', 'Plinio'),
            ('tempo', 'Tempus fugit', 'Il tempo fugge', 'Virgilio'),
            ('tempo', 'Carpe diem', 'Cogli l\'attimo', 'Orazio'),
            ('tempo', 'Vulnerant omnes, ultima necat', 'Tutte feriscono, l\'ultima uccide', '→ Ore'),
            ('tempo', 'Tempora mutantur, nos et mutamur in illis', 'I tempi cambiano e noi cambiamo con essi', ''),
            ('tempo', 'Omnia tempus habent', 'Ogni cosa ha il suo tempo', ''),
            ('tempo', 'Tempus omnia revelat', 'Il tempo rivela tutto', ''),
            ('tempo', 'Tempus edax rerum', 'Il tempo divora ogni cosa', 'Ovidio'),
            ('amicizia', 'Amicus certus in re incerta cernitur', 'L\'amico certo si riconosce nell\'incertezza', 'Cicerone'),
            ('amicizia', 'Amicus Plato, sed magis amica veritas', 'Platone è amico, ma più amica è la verità', 'Aristotele'),
            ('amicizia', 'Amicitia nisi inter bonos esse non potest', 'L\'amicizia può esistere solo tra uomini buoni', 'Cicerone'),
            ('amicizia', 'Idem velle atque idem nolle, ea demum firma amicitia est', 'Volere e non volere le stesse cose, questa è la vera amicizia', 'Sallustio'),
            ('amicizia', 'Amicus usque ad aras', 'Amico fino agli altari', ''),
            ('amicizia', 'Vera amicitia sempiterna est', 'La vera amicizia è eterna', ''),
            ('vita', 'Vita brevis, ars longa', 'La vita è breve, l\'arte è lunga', 'Ippocrate'),
            ('vita', 'Memento mori', 'Ricordati che devi morire', ''),
            ('vita', 'Dum spiro, spero', 'Finché respiro, spero', ''),
            ('vita', 'Vivere est cogitare', 'Vivere è pensare', 'Cicerone'),
            ('vita', 'Qui bene amat, bene castigat', 'Chi ama bene, corregge bene', ''),
            ('vita', 'Non scholae sed vitae discimus', 'Non impariamo per la scuola ma per la vita', 'Seneca'),
            ('vita', 'Beatus qui prodest quibus potest', 'Beato chi aiuta chi può', ''),
            ('saggezza', 'Cogito ergo sum', 'Penso dunque sono', 'Cartesio'),
            ('saggezza', 'Nosce te ipsum', 'Conosci te stesso', 'Socrate'),
            ('saggezza', 'Errare humanum est', 'Errare è umano', 'Seneca'),
            ('saggezza', 'Scientia potentia est', 'La conoscenza è potere', 'Bacone'),
            ('saggezza', 'Veritas vos liberabit', 'La verità vi renderà liberi', ''),
            ('saggezza', 'Sapere aude', 'Abbi il coraggio di sapere', 'Orazio'),
            ('saggezza', 'Nihil difficile volenti', 'Nulla è difficile per chi vuole', ''),
            ('destino', 'Fata viam invenient', 'Il destino troverà la sua strada', 'Virgilio'),
            ('destino', 'Ducunt volentem fata, nolentem trahunt', 'Il destino guida chi vuole e trascina chi non vuole', 'Seneca'),
            ('destino', 'Quod scripsi, scripsi', 'Ciò che ho scritto ho scritto', ''),
            ('coraggio', 'Audacia pro muro habetur', 'L\'audacia è considerata una difesa', 'Sallustio'),
            ('coraggio', 'Fortiter in re, suaviter in modo', 'Forte nei fatti, gentile nei modi', ''),
            ('coraggio', 'Nil desperandum', 'Non bisogna mai disperare', 'Orazio'),
            ('virtù', 'Virtus in actione consistit', 'La virtù consiste nell\'azione', ''),
            ('virtù', 'Virtus sola nobilitas', 'La virtù è la sola nobiltà', ''),
            ('virtù', 'Honos alit artes', 'L\'onore alimenta le arti', 'Cicerone'),
            ('sapienza', 'Mens sana in corpore sano', 'Mente sana in corpo sano', 'Giovenale'),
            ('sapienza', 'Gutta cavat lapidem', 'La goccia scava la pietra', 'Ovidio'),
            ('sapienza', 'Docendo discimus', 'Insegnando impariamo', 'Seneca'),
            ('verità', 'Magna est veritas et praevalebit', 'Grande è la verità e prevarrà', ''),
            ('verità', 'In vino veritas', 'Nel vino la verità', ''),
            ('verità', 'Veritas temporis filia', 'La verità è figlia del tempo', ''),
            ('guerra', 'Si vis pacem, para bellum', 'Se vuoi la pace prepara la guerra', ''),
            ('guerra', 'Inter arma silent leges', 'Tra le armi tacciono le leggi', 'Cicerone'),
            ('potere', 'Divide et impera', 'Dividi e governa', ''),
            ('potere', 'Panem et circenses', 'Pane e giochi', 'Giovenale'),
            ('natura', 'Natura nihil frustra facit', 'La natura non fa nulla invano', 'Aristotele'),
            ('natura', 'Omnia vincit amor', 'L\'amore vince tutto', 'Virgilio'),
            ('speranza', 'Spes ultima dea', 'La speranza è l\'ultima dea', ''),
            ('speranza', 'Post tenebras lux', 'Dopo le tenebre la luce', ''),
        ]

















        
        cursor.executemany(
            'INSERT INTO frasi_latine (tema, frase, traduzione, autore) VALUES (?, ?, ?, ?)',
            frasi_iniziali
        )
    
    conn.commit()
    conn.close()

def cerca_frasi_latine(tema):
    """Cerca frasi latine per tema"""
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT frase, traduzione, autore FROM frasi_latine 
        WHERE tema LIKE ? OR frase LIKE ? OR traduzione LIKE ?
        ORDER BY RANDOM()
    ''', (f'%{tema}%', f'%{tema}%', f'%{tema}%'))
    
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def tutte_frasi_latine():
    # Restituisce tutte le frasi latine 
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, tema, frase, traduzione, autore FROM frasi_latine ORDER BY tema, id')
    risultati = cursor.fetchall()
    conn.close()
    return risultati

def tutti_temi_latino():
    # Restituisce tutti i temi disponibili
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT tema FROM frasi_latine ORDER BY tema')
    temi = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return temi

def aggiungi_frase_latino_db(tema, frase, traduzione, autore="Anonimo"):
    # Aggiunge un nuovo proverbio al database
    conn = sqlite3.connect('frasi.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO frasi_latine (tema, frase, traduzione, autore)
        VALUES (?, ?, ?, ?)
    ''', (tema.lower(), frase, traduzione, autore))
    
    conn.commit()
    conn.close()
    return cursor.lastrowid