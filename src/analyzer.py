"""
=============================================================
Sistema di monitoraggio e analisi delle prestazioni

Modulo:
analyzer.py

Descrizione:
Coordina il caricamento delle metriche, il calcolo delle
statistiche descrittive e la generazione dei grafici.

Autore:
Gabriele Piccione
=============================================================
"""

import pandas as pd

from config import CSV_FILE
from graph_generator import genera_grafico
from statistics import stampa_statistiche


def carica_dati() -> pd.DataFrame:
    """
    Carica il file CSV prodotto dal monitoraggio.

    Returns:
        DataFrame contenente le metriche raccolte.

    Raises:
        FileNotFoundError: se il file CSV non esiste.
        ValueError: se il file CSV è vuoto.
    """

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"File non trovato: {CSV_FILE}\n"
            "Esegui prima il monitoraggio con: "
            "python src/main.py monitor"
        )

    dataframe = pd.read_csv(
        CSV_FILE,
        parse_dates=["timestamp"],
    )

    if dataframe.empty:
        raise ValueError("Il file CSV non contiene rilevazioni.")

    return dataframe


def main() -> None:
    """
    Avvia l'analisi del file CSV principale.
    """

    try:
        dataframe = carica_dati()

        stampa_statistiche(dataframe)

        genera_grafico(
            dataframe=dataframe,
            colonna="cpu",
            titolo="Utilizzo CPU nel tempo",
            nome_file="cpu.png",
        )

        genera_grafico(
            dataframe=dataframe,
            colonna="ram",
            titolo="Utilizzo RAM nel tempo",
            nome_file="ram.png",
        )

        genera_grafico(
            dataframe=dataframe,
            colonna="disco",
            titolo="Utilizzo disco nel tempo",
            nome_file="disco.png",
        )

        print("\nAnalisi completata correttamente.")

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as errore:
        print(f"\nErrore: {errore}")


if __name__ == "__main__":
    main()
