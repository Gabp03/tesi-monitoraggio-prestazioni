"""
==========================================================
main.py

Punto di ingresso principale dell'applicazione.

Permette di eseguire da un unico comando:
- monitoraggio manuale;
- esperimenti automatici;
- analisi del CSV principale;
- confronto degli scenari;
- generazione dei grafici comparativi;
- generazione del report PDF;
- esecuzione completa dell'intero flusso.

Autore: Gabriele Piccione
==========================================================
"""

import argparse
import subprocess
import sys
from pathlib import Path

# ==========================================================
# CONFIGURAZIONE
# ==========================================================

# Cartella che contiene gli script Python del progetto.
SRC_DIR = Path(__file__).resolve().parent

# Interprete Python attualmente in uso.
# In questo modo viene usato automaticamente quello
# dell'ambiente virtuale .venv.
PYTHON_EXECUTABLE = sys.executable

# Scenari sperimentali supportati.
SCENARI = [
    "baseline",
    "cpu",
    "ram",
    "disco",
    "combinato",
]


# ==========================================================
# ESECUZIONE DEGLI SCRIPT
# ==========================================================


def esegui_script(
    nome_script: str,
    argomenti: list[str] | None = None,
) -> None:
    """
    Esegue uno script Python del progetto.

    Args:
        nome_script: nome del file Python da eseguire.
        argomenti: eventuali argomenti da passare allo script.

    Raises:
        RuntimeError: se lo script non esiste o termina
        con un codice di errore.
    """

    percorso_script = SRC_DIR / nome_script

    if not percorso_script.exists():
        raise RuntimeError(f"Script non trovato: {percorso_script}")

    comando = [
        PYTHON_EXECUTABLE,
        str(percorso_script),
    ]

    if argomenti:
        comando.extend(argomenti)

    print("\n" + "=" * 70)
    print(f"ESECUZIONE: {' '.join(comando)}")
    print("=" * 70)

    try:
        subprocess.run(
            comando,
            check=True,
        )

    except subprocess.CalledProcessError as errore:
        raise RuntimeError(
            f"Lo script {nome_script} è terminato con errore. "
            f"Codice di uscita: {errore.returncode}"
        ) from errore


# ==========================================================
# COMANDI DELL'APPLICAZIONE
# ==========================================================


def comando_monitor() -> None:
    """
    Avvia il monitoraggio manuale fino alla pressione
    della combinazione CTRL+C.
    """

    esegui_script("monitor.py")


def comando_analyze() -> None:
    """
    Analizza il file metriche.csv e genera i grafici
    del monitoraggio manuale.
    """

    esegui_script("analyzer.py")


def comando_experiment(
    scenario: str,
    durata: int,
) -> None:
    """
    Esegue un singolo scenario sperimentale.

    Args:
        scenario: scenario da eseguire.
        durata: durata del test in secondi.
    """

    esegui_script(
        "experiment_runner.py",
        [
            scenario,
            "--duration",
            str(durata),
        ],
    )


def comando_compare() -> None:
    """
    Confronta tutti gli scenari sperimentali e genera
    il file riepilogo_scenari.csv.
    """

    esegui_script("compare_experiments.py")


def comando_graphs() -> None:
    """
    Genera i grafici comparativi degli scenari.
    """

    esegui_script("compare_graphs.py")


def comando_report() -> None:
    """
    Genera il report PDF finale.
    """

    esegui_script("report_generator.py")


def comando_all(durata: int) -> None:
    """
    Esegue l'intero flusso sperimentale.

    Il comando:
    1. esegue tutti gli scenari;
    2. confronta i risultati;
    3. genera i grafici;
    4. genera il report PDF.

    Args:
        durata: durata di ogni scenario in secondi.
    """

    print("\nAVVIO DEL FLUSSO COMPLETO")
    print(f"Durata di ogni scenario: {durata} secondi")

    for scenario in SCENARI:
        print("\n" + "#" * 70)
        print(f"SCENARIO: {scenario.upper()}")
        print("#" * 70)

        comando_experiment(
            scenario=scenario,
            durata=durata,
        )

    comando_compare()
    comando_graphs()
    comando_report()

    print("\n" + "=" * 70)
    print("FLUSSO COMPLETO TERMINATO CORRETTAMENTE")
    print("=" * 70)


# ==========================================================
# PARSER DEGLI ARGOMENTI
# ==========================================================


def crea_parser() -> argparse.ArgumentParser:
    """
    Crea il parser principale dell'applicazione.

    Returns:
        Parser configurato.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Sistema di monitoraggio, stress test " "e analisi delle prestazioni."
        )
    )

    sotto_parser = parser.add_subparsers(
        dest="comando",
        required=True,
    )

    # Comando monitor
    sotto_parser.add_parser(
        "monitor",
        help="Avvia il monitoraggio manuale.",
    )

    # Comando analyze
    sotto_parser.add_parser(
        "analyze",
        help="Analizza metriche.csv.",
    )

    # Comando compare
    sotto_parser.add_parser(
        "compare",
        help="Confronta gli scenari sperimentali.",
    )

    # Comando graphs
    sotto_parser.add_parser(
        "graphs",
        help="Genera i grafici comparativi.",
    )

    # Comando report
    sotto_parser.add_parser(
        "report",
        help="Genera il report PDF.",
    )

    # Comando experiment
    parser_experiment = sotto_parser.add_parser(
        "experiment",
        help="Esegue un singolo scenario.",
    )

    parser_experiment.add_argument(
        "scenario",
        choices=SCENARI,
        help="Scenario sperimentale da eseguire.",
    )

    parser_experiment.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Durata del test in secondi.",
    )

    # Comando all
    parser_all = sotto_parser.add_parser(
        "all",
        help="Esegue tutti gli scenari e genera il report.",
    )

    parser_all.add_argument(
        "--duration",
        type=int,
        default=30,
        help="Durata di ogni scenario in secondi.",
    )

    return parser


# ==========================================================
# FUNZIONE PRINCIPALE
# ==========================================================


def main() -> None:
    """
    Interpreta il comando scelto dall'utente.
    """

    parser = crea_parser()
    argomenti = parser.parse_args()

    try:
        if argomenti.comando == "monitor":
            comando_monitor()

        elif argomenti.comando == "analyze":
            comando_analyze()

        elif argomenti.comando == "experiment":
            if argomenti.duration <= 0:
                raise ValueError("La durata deve essere maggiore di zero.")

            comando_experiment(
                scenario=argomenti.scenario,
                durata=argomenti.duration,
            )

        elif argomenti.comando == "compare":
            comando_compare()

        elif argomenti.comando == "graphs":
            comando_graphs()

        elif argomenti.comando == "report":
            comando_report()

        elif argomenti.comando == "all":
            if argomenti.duration <= 0:
                raise ValueError("La durata deve essere maggiore di zero.")

            comando_all(
                durata=argomenti.duration,
            )

    except (RuntimeError, ValueError) as errore:
        print(f"\nErrore: {errore}")
        raise SystemExit(1) from errore


if __name__ == "__main__":
    main()
