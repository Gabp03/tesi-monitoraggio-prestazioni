"""
==========================================================
compare_graphs.py

Legge il file riepilogo_scenari.csv e genera grafici
comparativi tra i diversi scenari sperimentali.

Grafici prodotti:
- confronto CPU media;
- confronto RAM media;
- confronto occupazione disco;
- confronto attività di lettura su disco;
- confronto attività di scrittura su disco.

Autore: Gabriele Piccione
==========================================================
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import DATA_DIR, GRAFICI_DIR

# ==========================================================
# CONFIGURAZIONE DEI FILE
# ==========================================================

# File CSV prodotto da compare_experiments.py.
FILE_RIEPILOGO = DATA_DIR / "riepilogo_scenari.csv"


# ==========================================================
# CARICAMENTO DEI DATI
# ==========================================================


def carica_riepilogo() -> pd.DataFrame:
    """
    Carica il file contenente il confronto degli scenari.

    Returns:
        DataFrame con le statistiche di tutti gli scenari.

    Raises:
        FileNotFoundError: se il file non esiste.
        ValueError: se il file è vuoto.
    """

    # Verifica che il file riepilogativo esista.
    if not FILE_RIEPILOGO.exists():
        raise FileNotFoundError(
            f"File non trovato: {FILE_RIEPILOGO}\n"
            "Esegui prima: python src/compare_experiments.py"
        )

    # Lettura del CSV tramite Pandas.
    dataframe = pd.read_csv(FILE_RIEPILOGO)

    # Verifica che il file contenga almeno una riga.
    if dataframe.empty:
        raise ValueError("Il file riepilogo_scenari.csv è vuoto.")

    return dataframe


# ==========================================================
# GRAFICO A BARRE
# ==========================================================


def genera_grafico_barre(
    dataframe: pd.DataFrame,
    colonna: str,
    titolo: str,
    etichetta_y: str,
    nome_file: str,
) -> Path:
    """
    Genera un grafico a barre per confrontare una metrica.

    Args:
        dataframe: dati riepilogativi degli scenari.
        colonna: colonna numerica da rappresentare.
        titolo: titolo del grafico.
        etichetta_y: descrizione dell'asse verticale.
        nome_file: nome dell'immagine da creare.

    Returns:
        Percorso del grafico salvato.
    """

    # Verifica che la colonna richiesta esista.
    if colonna not in dataframe.columns:
        raise KeyError(
            f"La colonna '{colonna}' non è presente " "nel file riepilogativo."
        )

    # Creazione della figura.
    plt.figure(figsize=(10, 6))

    # Creazione del grafico a barre.
    barre = plt.bar(
        dataframe["scenario"],
        dataframe[colonna],
    )

    # Titolo e descrizione degli assi.
    plt.title(titolo)
    plt.xlabel("Scenario sperimentale")
    plt.ylabel(etichetta_y)

    # Griglia orizzontale per facilitare il confronto.
    plt.grid(
        axis="y",
        linestyle="--",
        alpha=0.5,
    )

    # Visualizzazione del valore sopra ogni barra.
    for barra in barre:
        altezza = barra.get_height()

        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altezza,
            f"{altezza:.2f}",
            ha="center",
            va="bottom",
        )

    # Adattamento automatico degli elementi.
    plt.tight_layout()

    # Creazione automatica della cartella grafici.
    GRAFICI_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Percorso completo del file immagine.
    percorso_output = GRAFICI_DIR / nome_file

    # Salvataggio in formato PNG.
    plt.savefig(
        percorso_output,
        dpi=150,
    )

    # Chiusura della figura per liberare memoria.
    plt.close()

    return percorso_output


# ==========================================================
# FUNZIONE PRINCIPALE
# ==========================================================


def main() -> None:
    """
    Genera tutti i grafici comparativi previsti.
    """

    try:
        # Caricamento del riepilogo degli scenari.
        dataframe = carica_riepilogo()

        grafici = [
            {
                "colonna": "cpu_media",
                "titolo": "Confronto dell'utilizzo medio della CPU",
                "etichetta_y": "CPU media (%)",
                "nome_file": "confronto_cpu_media.png",
            },
            {
                "colonna": "ram_media",
                "titolo": "Confronto dell'utilizzo medio della RAM",
                "etichetta_y": "RAM media (%)",
                "nome_file": "confronto_ram_media.png",
            },
            {
                "colonna": "disco_medio",
                "titolo": "Confronto dell'occupazione media del disco",
                "etichetta_y": "Spazio disco occupato (%)",
                "nome_file": "confronto_disco_medio.png",
            },
            {
                "colonna": "byte_letti_disco",
                "titolo": "Confronto dei byte letti dal disco",
                "etichetta_y": "Byte letti",
                "nome_file": "confronto_byte_letti_disco.png",
            },
            {
                "colonna": "byte_scritti_disco",
                "titolo": "Confronto dei byte scritti sul disco",
                "etichetta_y": "Byte scritti",
                "nome_file": "confronto_byte_scritti_disco.png",
            },
        ]

        # Generazione di tutti i grafici configurati.
        for configurazione in grafici:
            percorso = genera_grafico_barre(
                dataframe=dataframe,
                colonna=configurazione["colonna"],
                titolo=configurazione["titolo"],
                etichetta_y=configurazione["etichetta_y"],
                nome_file=configurazione["nome_file"],
            )

            print(f"Grafico salvato: {percorso}")

        print("\nGrafici comparativi generati correttamente.")

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as errore:
        print(f"\nErrore: {errore}")


if __name__ == "__main__":
    main()
