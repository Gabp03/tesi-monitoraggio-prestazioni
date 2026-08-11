"""
=============================================================
Sistema di monitoraggio e analisi delle prestazioni

Modulo:
config.py

Descrizione:
Contiene tutti i percorsi, i nomi dei file e i parametri
utilizzati dall'intero progetto.

Autore:
Gabriele Piccione
=============================================================
"""

from pathlib import Path

# ==========================================================
# PERCORSI PRINCIPALI DEL PROGETTO
# ==========================================================

# Percorso assoluto della cartella principale:
# /home/gabriele/tesi-monitoraggio
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Cartella che conterrà i file CSV prodotti dai test.
DATA_DIR: Path = BASE_DIR / "data"

# Cartella destinata ai grafici generati.
GRAFICI_DIR: Path = BASE_DIR / "grafici"

# Cartella destinata alla documentazione del progetto.
DOCUMENTAZIONE_DIR: Path = BASE_DIR / "documentazione"

# File CSV principale prodotto dal monitoraggio.
CSV_FILE: Path = DATA_DIR / "metriche.csv"


# ==========================================================
# PARAMETRI DI MONITORAGGIO
# ==========================================================

# Tempo, espresso in secondi, tra una rilevazione e la successiva.
SAMPLE_INTERVAL: int = 1

# ==========================================================
# FINE CONFIGURAZIONE
# ==========================================================
