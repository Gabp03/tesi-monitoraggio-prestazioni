"""
=============================================================
Sistema di monitoraggio e analisi delle prestazioni

Modulo:
statistics.py

Descrizione:
Contiene le funzioni dedicate al calcolo e alla stampa
delle statistiche descrittive delle metriche raccolte.

Autore:
Gabriele Piccione
=============================================================
"""

import pandas as pd

METRICHE_PERCENTUALI: tuple[str, ...] = (
    "cpu",
    "ram",
    "disco",
)


def calcola_statistiche(
    dataframe: pd.DataFrame,
    metrica: str,
) -> dict[str, float]:
    """
    Calcola le principali statistiche descrittive
    per una singola metrica.

    Args:
        dataframe: insieme delle rilevazioni raccolte.
        metrica: nome della colonna da analizzare.

    Returns:
        Dizionario contenente media, minimo, massimo
        e deviazione standard.

    Raises:
        KeyError: se la metrica non è presente nel DataFrame.
    """

    if metrica not in dataframe.columns:
        raise KeyError(f"La metrica '{metrica}' non è presente nei dati.")

    valori = dataframe[metrica]

    return {
        "media": float(valori.mean()),
        "minimo": float(valori.min()),
        "massimo": float(valori.max()),
        "deviazione_standard": float(valori.std()),
    }


def stampa_statistiche(
    dataframe: pd.DataFrame,
) -> None:
    """
    Calcola e stampa le statistiche descrittive
    delle metriche principali.

    Args:
        dataframe: insieme delle rilevazioni raccolte.
    """

    print("\nSTATISTICHE DESCRITTIVE")
    print("=" * 50)

    for metrica in METRICHE_PERCENTUALI:
        statistiche = calcola_statistiche(
            dataframe=dataframe,
            metrica=metrica,
        )

        print(f"\n{metrica.upper()}")
        print(f"Media:               " f"{statistiche['media']:.2f}%")
        print(f"Minimo:              " f"{statistiche['minimo']:.2f}%")
        print(f"Massimo:             " f"{statistiche['massimo']:.2f}%")
        print(f"Deviazione standard: " f"{statistiche['deviazione_standard']:.2f}")
