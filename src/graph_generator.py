"""
=============================================================
Sistema di monitoraggio e analisi delle prestazioni

Modulo:
graph_generator.py

Descrizione:
Contiene le funzioni dedicate alla generazione e al salvataggio
dei grafici temporali delle metriche raccolte.

Autore:
Gabriele Piccione
=============================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import GRAFICI_DIR


def genera_grafico(
    dataframe: pd.DataFrame,
    colonna: str,
    titolo: str,
    nome_file: str,
) -> Path:
    """
    Genera e salva un grafico temporale per una metrica.

    Args:
        dataframe: insieme delle rilevazioni raccolte.
        colonna: nome della colonna da rappresentare.
        titolo: titolo del grafico.
        nome_file: nome del file PNG da creare.

    Returns:
        Percorso del grafico generato.

    Raises:
        KeyError: se la colonna non è presente nei dati.
    """

    if colonna not in dataframe.columns:
        raise KeyError(f"La colonna '{colonna}' non è presente nei dati.")

    if "timestamp" not in dataframe.columns:
        raise KeyError("La colonna 'timestamp' non è presente nei dati.")

    GRAFICI_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    percorso = GRAFICI_DIR / nome_file

    plt.figure(figsize=(10, 5))
    plt.plot(
        dataframe["timestamp"],
        dataframe[colonna],
    )
    plt.title(titolo)
    plt.xlabel("Tempo")
    plt.ylabel("Utilizzo (%)")
    plt.xticks(rotation=30)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(
        percorso,
        dpi=150,
    )
    plt.close()

    print(f"Grafico salvato: {percorso}")

    return percorso
