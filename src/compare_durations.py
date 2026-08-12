from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "test_durata"
OUTPUT_FILE = DATA_DIR / "riepilogo_durate.csv"

SCENARI = ["baseline", "cpu", "ram", "disco", "combinato"]
DURATE = [30, 60, 120]


def percorso_csv(scenario: str, durata: int) -> Path:
    if durata == 30:
        return DATA_DIR / f"{scenario}_originale_30s.csv"

    return DATA_DIR / f"{scenario}_{durata}s.csv"


def incremento(serie: pd.Series) -> float:
    if serie.empty:
        return 0.0

    return float(serie.iloc[-1] - serie.iloc[0])


def main() -> None:
    risultati = []

    for durata in DURATE:
        for scenario in SCENARI:
            percorso = percorso_csv(scenario, durata)

            if not percorso.exists():
                print(f"File mancante: {percorso}")
                continue

            df = pd.read_csv(percorso)

            risultati.append(
                {
                    "scenario": scenario,
                    "durata": durata,
                    "campioni": len(df),
                    "cpu_media": df["cpu"].mean(),
                    "cpu_massima": df["cpu"].max(),
                    "cpu_dev_std": df["cpu"].std(),
                    "ram_media": df["ram"].mean(),
                    "ram_massima": df["ram"].max(),
                    "ram_dev_std": df["ram"].std(),
                    "disco_medio": df["disco"].mean(),
                    "byte_letti_disco": incremento(df["byte_letti_disco"]),
                    "byte_scritti_disco": incremento(df["byte_scritti_disco"]),
                    "letture_disco": incremento(df["letture_disco"]),
                    "scritture_disco": incremento(df["scritture_disco"]),
                }
            )

    riepilogo = pd.DataFrame(risultati)

    riepilogo.to_csv(OUTPUT_FILE, index=False)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)

    print("\nCONFRONTO DURATE 30 / 60 / 120 SECONDI")
    print("=" * 100)

    colonne = [
        "scenario",
        "durata",
        "campioni",
        "cpu_media",
        "ram_media",
        "disco_medio",
        "byte_scritti_disco",
    ]

    print(riepilogo[colonne].round(2).to_string(index=False))

    print(f"\nRiepilogo salvato in:\n{OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    