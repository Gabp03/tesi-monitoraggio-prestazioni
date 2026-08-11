"""
==========================================================
compare_experiments.py

Legge i file CSV generati dagli esperimenti, calcola le
statistiche principali e crea una tabella comparativa.

Scenari confrontati:
- baseline;
- cpu;
- ram;
- disco;
- combinato.

Autore: Gabriele Piccione
==========================================================
"""

import pandas as pd

from config import DATA_DIR

# ==========================================================
# CONFIGURAZIONE
# ==========================================================

# Elenco degli scenari da confrontare.
SCENARI = [
    "baseline",
    "cpu",
    "ram",
    "disco",
    "combinato",
]

# File CSV finale contenente il riepilogo.
FILE_RIEPILOGO = DATA_DIR / "riepilogo_scenari.csv"


# ==========================================================
# CARICAMENTO DATI
# ==========================================================


def carica_scenario(scenario: str) -> pd.DataFrame:
    """
    Carica il file CSV relativo a uno scenario.

    Args:
        scenario: nome dello scenario da caricare.

    Returns:
        DataFrame contenente le rilevazioni dello scenario.

    Raises:
        FileNotFoundError: se il file CSV non esiste.
        ValueError: se il file è vuoto.
    """

    file_scenario = DATA_DIR / f"metriche_{scenario}.csv"

    if not file_scenario.exists():
        raise FileNotFoundError(f"File non trovato: {file_scenario}")

    dataframe = pd.read_csv(
        file_scenario,
        parse_dates=["timestamp"],
    )

    if dataframe.empty:
        raise ValueError(f"Il file dello scenario '{scenario}' è vuoto.")

    return dataframe


# ==========================================================
# CALCOLO DELLE VARIAZIONI
# ==========================================================


def calcola_incremento(
    serie: pd.Series,
) -> float:
    """
    Calcola la differenza tra ultimo e primo valore.

    È utile per contatori cumulativi come:
    - byte letti e scritti su disco;
    - byte inviati e ricevuti in rete.

    Args:
        serie: colonna numerica del DataFrame.

    Returns:
        Incremento osservato durante l'esperimento.
    """

    if serie.empty:
        return 0.0

    return float(serie.iloc[-1] - serie.iloc[0])


# ==========================================================
# ANALISI DEL SINGOLO SCENARIO
# ==========================================================


def analizza_scenario(
    scenario: str,
    dataframe: pd.DataFrame,
) -> dict:
    """
    Calcola le statistiche riepilogative di uno scenario.

    Args:
        scenario: nome dello scenario.
        dataframe: dati raccolti durante il test.

    Returns:
        Dizionario contenente le statistiche calcolate.
    """

    return {
        "scenario": scenario,
        # CPU
        "cpu_media": dataframe["cpu"].mean(),
        "cpu_massima": dataframe["cpu"].max(),
        "cpu_dev_std": dataframe["cpu"].std(),
        # RAM
        "ram_media": dataframe["ram"].mean(),
        "ram_massima": dataframe["ram"].max(),
        "ram_dev_std": dataframe["ram"].std(),
        # Swap e spazio disco
        "swap_media": dataframe["swap"].mean(),
        "disco_medio": dataframe["disco"].mean(),
        # Attività disco osservata durante il test
        "byte_letti_disco": calcola_incremento(dataframe["byte_letti_disco"]),
        "byte_scritti_disco": calcola_incremento(dataframe["byte_scritti_disco"]),
        "letture_disco": calcola_incremento(dataframe["letture_disco"]),
        "scritture_disco": calcola_incremento(dataframe["scritture_disco"]),
        # Traffico di rete osservato durante il test
        "bytes_inviati": calcola_incremento(dataframe["bytes_inviati"]),
        "bytes_ricevuti": calcola_incremento(dataframe["bytes_ricevuti"]),
        # Numero di campioni raccolti
        "campioni": len(dataframe),
    }


# ==========================================================
# FORMATTAZIONE OUTPUT
# ==========================================================


def stampa_tabella(riepilogo: pd.DataFrame) -> None:
    """
    Stampa nel terminale una tabella comparativa compatta.

    Args:
        riepilogo: DataFrame contenente i risultati.
    """

    colonne = [
        "scenario",
        "cpu_media",
        "cpu_massima",
        "ram_media",
        "ram_massima",
        "disco_medio",
        "swap_media",
    ]

    tabella = riepilogo[colonne].copy()

    colonne_numeriche = [
        "cpu_media",
        "cpu_massima",
        "ram_media",
        "ram_massima",
        "disco_medio",
        "swap_media",
    ]

    tabella[colonne_numeriche] = tabella[colonne_numeriche].round(2)

    print("\nCONFRONTO DEGLI SCENARI")
    print("=" * 90)
    print(tabella.to_string(index=False))


# ==========================================================
# FUNZIONE PRINCIPALE
# ==========================================================


def main() -> None:
    """
    Carica tutti gli scenari, calcola le statistiche
    e salva il riepilogo finale in formato CSV.
    """

    risultati: list[dict] = []

    try:
        for scenario in SCENARI:
            print(f"Analisi scenario: {scenario}")

            dataframe = carica_scenario(scenario)

            risultato = analizza_scenario(
                scenario=scenario,
                dataframe=dataframe,
            )

            risultati.append(risultato)

        riepilogo = pd.DataFrame(risultati)

        DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        riepilogo.to_csv(
            FILE_RIEPILOGO,
            index=False,
        )

        stampa_tabella(riepilogo)

        print("\nRiepilogo salvato correttamente:")
        print(FILE_RIEPILOGO)

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as errore:
        print(f"\nErrore durante il confronto: {errore}")


if __name__ == "__main__":
    main()
