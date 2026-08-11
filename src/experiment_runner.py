"""
==========================================================
experiment_runner.py

Coordina un esperimento completo:

1. avvia eventualmente uno stress test;
2. raccoglie le metriche durante il test;
3. salva i risultati in un file CSV dedicato.

Scenari supportati:
- baseline;
- cpu;
- ram;
- disco;
- combinato.

Autore: Gabriele Piccione
==========================================================
"""

import argparse
import threading
import time
from pathlib import Path

import pandas as pd

from collector import raccogli_metriche
from config import DATA_DIR
from stress_manager import esegui_scenario


def esegui_stress_in_thread(
    scenario: str,
    durata: int,
) -> threading.Thread | None:
    """
    Avvia lo stress test in un thread separato.

    Per lo scenario baseline non viene avviato alcun carico.

    Args:
        scenario: tipo di scenario.
        durata: durata del test in secondi.

    Returns:
        Thread dello stress test oppure None per baseline.
    """

    if scenario == "baseline":
        return None

    thread = threading.Thread(
        target=esegui_scenario,
        args=(scenario, durata),
        daemon=True,
    )

    thread.start()

    return thread


def raccogli_dati_esperimento(
    scenario: str,
    durata: int,
) -> list[dict]:
    """
    Raccoglie le metriche durante l'esperimento.

    Args:
        scenario: nome dello scenario.
        durata: durata del test.

    Returns:
        Lista delle rilevazioni raccolte.
    """

    dati: list[dict] = []

    thread_stress = esegui_stress_in_thread(
        scenario=scenario,
        durata=durata,
    )

    # Memorizza l'istante di inizio dell'esperimento.
    tempo_inizio = time.monotonic()

    while True:
        # Calcola il tempo trascorso.
        tempo_trascorso = time.monotonic() - tempo_inizio

        # Interrompe la raccolta dopo la durata richiesta.
        if tempo_trascorso >= durata:
            break

        metrica = raccogli_metriche()

        # Aggiunge informazioni sullo scenario.
        metrica["scenario"] = scenario
        metrica["secondi_trascorsi"] = round(
            tempo_trascorso,
            2,
        )

        dati.append(metrica)

        print(
            f"Scenario: {scenario:<10} "
            f"CPU: {metrica['cpu']:5.1f}%   "
            f"RAM: {metrica['ram']:5.1f}%   "
            f"DISCO: {metrica['disco']:5.1f}%"
        )

    # Attende la conclusione dello stress test, se presente.
    if thread_stress is not None:
        thread_stress.join()

    return dati


def salva_risultati(
    dati: list[dict],
    scenario: str,
) -> Path:
    """
    Salva i risultati dell'esperimento in un CSV separato.

    Args:
        dati: metriche raccolte.
        scenario: nome dello scenario.

    Returns:
        Percorso del file CSV creato.
    """

    if not dati:
        raise ValueError("Nessuna metrica raccolta durante l'esperimento.")

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_output = DATA_DIR / f"metriche_{scenario}.csv"

    dataframe = pd.DataFrame(dati)

    dataframe.to_csv(
        file_output,
        index=False,
    )

    return file_output


def crea_parser() -> argparse.ArgumentParser:
    """
    Configura gli argomenti da linea di comando.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Esegue uno scenario sperimentale e raccoglie "
            "automaticamente le metriche."
        )
    )

    parser.add_argument(
        "scenario",
        choices=[
            "baseline",
            "cpu",
            "ram",
            "disco",
            "combinato",
        ],
        help="Scenario da eseguire.",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Durata del test in secondi.",
    )

    return parser


def main() -> None:
    """
    Avvia l'esperimento completo.
    """

    parser = crea_parser()
    argomenti = parser.parse_args()

    if argomenti.duration <= 0:
        print("Errore: la durata deve essere maggiore di zero.")
        return

    print("=" * 60)
    print(" AVVIO ESPERIMENTO AUTOMATICO")
    print(f" Scenario: {argomenti.scenario}")
    print(f" Durata: {argomenti.duration} secondi")
    print("=" * 60)

    try:
        dati = raccogli_dati_esperimento(
            scenario=argomenti.scenario,
            durata=argomenti.duration,
        )

        file_output = salva_risultati(
            dati=dati,
            scenario=argomenti.scenario,
        )

        print("\nEsperimento completato correttamente.")
        print(f"Rilevazioni raccolte: {len(dati)}")
        print(f"File salvato: {file_output}")

    except (ValueError, RuntimeError) as errore:
        print(f"\nErrore: {errore}")


if __name__ == "__main__":
    main()
