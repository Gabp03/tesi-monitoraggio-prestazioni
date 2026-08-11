"""
==========================================================
stress_manager.py

Gestisce l'esecuzione automatica degli stress test tramite
lo strumento stress-ng.

Gli scenari attualmente supportati sono:
- CPU;
- RAM;
- disco;
- CPU e RAM contemporaneamente.

Autore: Gabriele Piccione
==========================================================
"""

import argparse
import os
import subprocess
from typing import Final

# ==========================================================
# CONFIGURAZIONE
# ==========================================================

# Durata predefinita di uno stress test, espressa in secondi.
DURATA_PREDEFINITA: Final[int] = 30

# Numero di core logici disponibili nella macchina virtuale.
NUMERO_CPU: Final[int] = os.cpu_count() or 1


# ==========================================================
# VALIDAZIONE
# ==========================================================


def valida_durata(durata: int) -> None:
    """
    Verifica che la durata dello stress test sia valida.

    Args:
        durata: durata del test espressa in secondi.

    Raises:
        ValueError: se la durata è minore o uguale a zero.
    """

    if durata <= 0:
        raise ValueError("La durata dello stress test deve essere " "maggiore di zero.")


# ==========================================================
# ESECUZIONE DEL COMANDO
# ==========================================================


def esegui_comando(comando: list[str]) -> None:
    """
    Esegue un comando stress-ng e attende il suo completamento.

    Args:
        comando: lista contenente comando e relativi argomenti.

    Raises:
        RuntimeError: se stress-ng non è installato oppure
        se il comando termina con un errore.
    """

    print("\nComando eseguito:")
    print(" ".join(comando))
    print()

    try:
        # check=True genera un'eccezione se il comando
        # termina con un codice di uscita diverso da zero.
        subprocess.run(
            comando,
            check=True,
        )

    except FileNotFoundError as errore:
        raise RuntimeError(
            "stress-ng non è installato o non è disponibile " "nel PATH del sistema."
        ) from errore

    except subprocess.CalledProcessError as errore:
        raise RuntimeError(
            f"Lo stress test è terminato con errore. "
            f"Codice di uscita: {errore.returncode}"
        ) from errore


# ==========================================================
# STRESS TEST CPU
# ==========================================================


def esegui_stress_cpu(durata: int) -> None:
    """
    Genera un carico intensivo su tutti i core della CPU.

    Args:
        durata: durata del test in secondi.
    """

    valida_durata(durata)

    print("=" * 50)
    print(" AVVIO STRESS TEST CPU")
    print(f" Core utilizzati: {NUMERO_CPU}")
    print(f" Durata: {durata} secondi")
    print("=" * 50)

    comando = [
        "stress-ng",
        "--cpu",
        str(NUMERO_CPU),
        "--cpu-method",
        "all",
        "--timeout",
        f"{durata}s",
        "--metrics-brief",
    ]

    esegui_comando(comando)

    print("\nStress test CPU completato.")


# ==========================================================
# STRESS TEST RAM
# ==========================================================


def esegui_stress_ram(durata: int) -> None:
    """
    Genera un carico sulla memoria RAM.

    Viene utilizzato un processo virtual-memory che occupa
    il 70% della memoria disponibile.

    Args:
        durata: durata del test in secondi.
    """

    valida_durata(durata)

    print("=" * 50)
    print(" AVVIO STRESS TEST RAM")
    print(" Memoria utilizzata: 70%")
    print(f" Durata: {durata} secondi")
    print("=" * 50)

    comando = [
        "stress-ng",
        "--vm",
        "1",
        "--vm-bytes",
        "70%",
        "--vm-keep",
        "--timeout",
        f"{durata}s",
        "--metrics-brief",
    ]

    esegui_comando(comando)

    print("\nStress test RAM completato.")


# ==========================================================
# STRESS TEST DISCO
# ==========================================================


def esegui_stress_disco(durata: int) -> None:
    """
    Genera operazioni intensive di lettura e scrittura
    sul disco tramite stress-ng.

    Args:
        durata: durata del test in secondi.
    """

    valida_durata(durata)

    print("=" * 50)
    print(" AVVIO STRESS TEST DISCO")
    print(f" Durata: {durata} secondi")
    print("=" * 50)

    comando = [
        "stress-ng",
        "--hdd",
        "1",
        "--hdd-bytes",
        "512M",
        "--timeout",
        f"{durata}s",
        "--metrics-brief",
    ]

    esegui_comando(comando)

    print("\nStress test disco completato.")


# ==========================================================
# STRESS TEST COMBINATO
# ==========================================================


def esegui_stress_combinato(durata: int) -> None:
    """
    Genera contemporaneamente carico su CPU e RAM.

    Args:
        durata: durata del test in secondi.
    """

    valida_durata(durata)

    print("=" * 50)
    print(" AVVIO STRESS TEST COMBINATO")
    print(f" Core CPU utilizzati: {NUMERO_CPU}")
    print(" Memoria utilizzata: 60%")
    print(f" Durata: {durata} secondi")
    print("=" * 50)

    comando = [
        "stress-ng",
        "--cpu",
        str(NUMERO_CPU),
        "--vm",
        "1",
        "--vm-bytes",
        "60%",
        "--vm-keep",
        "--timeout",
        f"{durata}s",
        "--metrics-brief",
    ]

    esegui_comando(comando)

    print("\nStress test combinato completato.")


# ==========================================================
# SELEZIONE DELLO SCENARIO
# ==========================================================


def esegui_scenario(scenario: str, durata: int) -> None:
    """
    Avvia lo stress test corrispondente allo scenario scelto.

    Args:
        scenario: nome dello scenario da eseguire.
        durata: durata del test in secondi.

    Raises:
        ValueError: se lo scenario non è supportato.
    """

    scenari = {
        "cpu": esegui_stress_cpu,
        "ram": esegui_stress_ram,
        "disco": esegui_stress_disco,
        "combinato": esegui_stress_combinato,
    }

    funzione_test = scenari.get(scenario)

    if funzione_test is None:
        raise ValueError(f"Scenario non supportato: {scenario}")

    funzione_test(durata)


# ==========================================================
# ARGOMENTI DA TERMINALE
# ==========================================================


def crea_parser() -> argparse.ArgumentParser:
    """
    Crea il parser degli argomenti da linea di comando.

    Returns:
        argparse.ArgumentParser: parser configurato.
    """

    parser = argparse.ArgumentParser(
        description=("Esegue stress test automatici su CPU, RAM e disco.")
    )

    parser.add_argument(
        "scenario",
        choices=["cpu", "ram", "disco", "combinato"],
        help="Scenario di stress test da eseguire.",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=DURATA_PREDEFINITA,
        help=(
            "Durata del test in secondi. " f"Valore predefinito: {DURATA_PREDEFINITA}."
        ),
    )

    return parser


# ==========================================================
# FUNZIONE PRINCIPALE
# ==========================================================


def main() -> None:
    """
    Legge gli argomenti da terminale e avvia lo stress test.
    """

    parser = crea_parser()
    argomenti = parser.parse_args()

    try:
        esegui_scenario(
            scenario=argomenti.scenario,
            durata=argomenti.duration,
        )

    except (ValueError, RuntimeError) as errore:
        print(f"\nErrore: {errore}")


if __name__ == "__main__":
    main()
