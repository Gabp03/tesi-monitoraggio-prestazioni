from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "test_durata" / "riepilogo_durate.csv"
OUTPUT_DIR = BASE_DIR / "grafici" / "durate"


def salva_grafico(x, y, titolo, ylabel, nome_file):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker="o")
    plt.xlabel("Durata esperimento (s)")
    plt.ylabel(ylabel)
    plt.title(titolo)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / nome_file, dpi=150)
    plt.close()

    print(f"Grafico salvato: {OUTPUT_DIR / nome_file}")


def main():
    df = pd.read_csv(CSV_FILE)

    cpu = df[df["scenario"] == "cpu"]
    ram = df[df["scenario"] == "ram"]
    disco = df[df["scenario"] == "disco"]
    combinato = df[df["scenario"] == "combinato"]

    salva_grafico(
        cpu["durata"],
        cpu["cpu_media"],
        "Utilizzo medio CPU al variare della durata",
        "CPU media (%)",
        "cpu_durata.png",
    )

    salva_grafico(
        ram["durata"],
        ram["ram_media"],
        "Utilizzo medio RAM al variare della durata",
        "RAM media (%)",
        "ram_durata.png",
    )

    salva_grafico(
        disco["durata"],
        disco["byte_scritti_disco"] / (1024**3),
        "Dati scritti su disco al variare della durata",
        "Dati scritti (GiB)",
        "disco_durata.png",
    )

    salva_grafico(
        combinato["durata"],
        combinato["ram_media"],
        "RAM nello scenario combinato al variare della durata",
        "RAM media (%)",
        "combinato_ram_durata.png",
    )


if __name__ == "__main__":
    main()
    