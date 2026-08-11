"""
==========================================================
monitor.py

Coordina il monitoraggio delle prestazioni del sistema.

Il programma utilizza:
- collector.py per raccogliere le metriche;
- config.py per percorsi e configurazione;
- Pandas per salvare i dati in formato CSV.

Autore: Gabriele Piccione
==========================================================
"""

import pandas as pd

from collector import raccogli_metriche
from config import CSV_FILE, DATA_DIR


def salva_metriche(dati: list[dict]) -> None:
    """
    Salva le rilevazioni raccolte in un file CSV.

    Args:
        dati: lista di dizionari contenenti le metriche.
    """

    # Crea la cartella data se non è già presente.
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Converte la lista di rilevazioni in un DataFrame Pandas.
    dataframe = pd.DataFrame(dati)

    # Salva il DataFrame nel file CSV configurato.
    dataframe.to_csv(CSV_FILE, index=False)


def stampa_rilevazione(metrica: dict) -> None:
    """
    Mostra nel terminale i valori principali
    della rilevazione corrente.

    Args:
        metrica: dizionario contenente una rilevazione.
    """

    print(
        f"CPU: {metrica['cpu']:5.1f}%   "
        f"RAM: {metrica['ram']:5.1f}%   "
        f"DISCO: {metrica['disco']:5.1f}%"
    )


def main() -> None:
    """
    Avvia il ciclo di monitoraggio.

    Le metriche vengono raccolte fino alla pressione
    della combinazione CTRL+C.
    """

    # Lista che conterrà tutte le rilevazioni.
    dati: list[dict] = []

    print("=" * 50)
    print(" Monitoraggio delle prestazioni avviato")
    print(" Premi CTRL+C per terminare")
    print("=" * 50)
    print()

    try:
        # Ciclo continuo di raccolta delle metriche.
        while True:
            metrica = raccogli_metriche()
            dati.append(metrica)
            stampa_rilevazione(metrica)

    except KeyboardInterrupt:
        print("\nMonitoraggio terminato.")

        # Evita di creare un CSV vuoto se il programma
        # viene interrotto prima della prima rilevazione.
        if not dati:
            print("Nessuna metrica raccolta. File non creato.")
            return

        print("Salvataggio dati...")
        salva_metriche(dati)

        print("File salvato correttamente:")
        print(CSV_FILE)


if __name__ == "__main__":
    main()
