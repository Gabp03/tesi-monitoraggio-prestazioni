"""
==========================================================
report_generator.py

Genera automaticamente un report PDF contenente:

- descrizione del progetto;
- tabella comparativa degli scenari;
- grafici generati dal programma;
- osservazioni automatiche sui risultati.

Autore: Gabriele Piccione
==========================================================
"""

from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from config import DATA_DIR, DOCUMENTAZIONE_DIR, GRAFICI_DIR

# ==========================================================
# CONFIGURAZIONE DEI FILE
# ==========================================================

# File CSV prodotto dal confronto degli esperimenti.
FILE_RIEPILOGO = DATA_DIR / "riepilogo_scenari.csv"

# File PDF finale.
FILE_REPORT = DOCUMENTAZIONE_DIR / "report_prestazioni.pdf"

# Grafici principali da inserire nel documento.
GRAFICO_CPU = GRAFICI_DIR / "confronto_cpu_media.png"
GRAFICO_RAM = GRAFICI_DIR / "confronto_ram_media.png"
GRAFICO_DISCO = GRAFICI_DIR / "confronto_disco_medio.png"
GRAFICO_LETTURE = GRAFICI_DIR / "confronto_byte_letti_disco.png"
GRAFICO_SCRITTURE = GRAFICI_DIR / "confronto_byte_scritti_disco.png"


# ==========================================================
# CARICAMENTO DATI
# ==========================================================


def carica_riepilogo() -> pd.DataFrame:
    """
    Carica il file riepilogativo degli esperimenti.

    Returns:
        DataFrame contenente i risultati degli scenari.

    Raises:
        FileNotFoundError: se il file non esiste.
        ValueError: se il file è vuoto.
    """

    if not FILE_RIEPILOGO.exists():
        raise FileNotFoundError(
            f"File non trovato: {FILE_RIEPILOGO}\n"
            "Esegui prima: python src/compare_experiments.py"
        )

    dataframe = pd.read_csv(FILE_RIEPILOGO)

    if dataframe.empty:
        raise ValueError("Il file riepilogo_scenari.csv è vuoto.")

    return dataframe


# ==========================================================
# CREAZIONE DELLA TABELLA
# ==========================================================


def crea_tabella_riepilogo(
    dataframe: pd.DataFrame,
) -> Table:
    """
    Crea una tabella PDF contenente i risultati principali.

    Args:
        dataframe: riepilogo degli scenari.

    Returns:
        Tabella ReportLab pronta per essere inserita nel PDF.
    """

    intestazione = [
        "Scenario",
        "CPU media",
        "CPU max",
        "RAM media",
        "RAM max",
        "Disco medio",
    ]

    dati_tabella = [intestazione]

    for _, riga in dataframe.iterrows():
        dati_tabella.append(
            [
                str(riga["scenario"]).capitalize(),
                f"{riga['cpu_media']:.2f}%",
                f"{riga['cpu_massima']:.2f}%",
                f"{riga['ram_media']:.2f}%",
                f"{riga['ram_massima']:.2f}%",
                f"{riga['disco_medio']:.2f}%",
            ]
        )

    tabella = Table(
        dati_tabella,
        colWidths=[
            2.7 * cm,
            2.4 * cm,
            2.4 * cm,
            2.4 * cm,
            2.4 * cm,
            2.6 * cm,
        ],
        repeatRows=1,
    )

    tabella.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#D9EAF7"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.black,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER",
                ),
                (
                    "ALIGN",
                    (0, 0),
                    (-1, 0),
                    "CENTER",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F5F5F5"),
                    ],
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    8,
                ),
            ]
        )
    )

    return tabella


# ==========================================================
# GENERAZIONE DELLE CONCLUSIONI
# ==========================================================


def genera_conclusioni(
    dataframe: pd.DataFrame,
) -> list[str]:
    """
    Genera osservazioni automatiche in base ai risultati.

    Args:
        dataframe: riepilogo degli scenari.

    Returns:
        Lista di frasi descrittive.
    """

    dati = dataframe.set_index("scenario")

    conclusioni: list[str] = []

    if "baseline" in dati.index and "cpu" in dati.index:
        incremento_cpu = (
            dati.loc["cpu", "cpu_media"] - dati.loc["baseline", "cpu_media"]
        )

        conclusioni.append(
            "Lo scenario CPU ha incrementato l'utilizzo medio "
            f"del processore di {incremento_cpu:.2f} punti "
            "percentuali rispetto alla baseline."
        )

    if "baseline" in dati.index and "ram" in dati.index:
        incremento_ram = (
            dati.loc["ram", "ram_media"] - dati.loc["baseline", "ram_media"]
        )

        conclusioni.append(
            "Lo scenario RAM ha incrementato l'utilizzo medio "
            f"della memoria di {incremento_ram:.2f} punti "
            "percentuali rispetto alla baseline."
        )

    if "combinato" in dati.index:
        conclusioni.append(
            "Lo scenario combinato rappresenta il carico più "
            "gravoso, poiché sottopone contemporaneamente CPU "
            "e memoria RAM a stress."
        )

    if "disco" in dati.index and "baseline" in dati.index:
        byte_scritti_disso = dati.loc[
            "disco",
            "byte_scritti_disco",
        ]

        byte_scritti_baseline = dati.loc[
            "baseline",
            "byte_scritti_disco",
        ]

        differenza_scritture = byte_scritti_disso - byte_scritti_baseline

        conclusioni.append(
            "Il test disco ha prodotto un incremento delle "
            "scritture pari a "
            f"{differenza_scritture:,.0f} byte rispetto "
            "alla baseline."
        )

    return conclusioni


# ==========================================================
# INSERIMENTO DEI GRAFICI
# ==========================================================


def aggiungi_grafico(
    elementi: list,
    percorso: Path,
    titolo: str,
    stile_titolo: ParagraphStyle,
) -> None:
    """
    Inserisce un grafico nel report, se il file esiste.

    Args:
        elementi: lista degli elementi del PDF.
        percorso: percorso dell'immagine.
        titolo: titolo del grafico.
        stile_titolo: stile ReportLab per il titolo.
    """

    if not percorso.exists():
        return

    elementi.append(
        Paragraph(
            titolo,
            stile_titolo,
        )
    )

    elementi.append(Spacer(1, 0.25 * cm))

    immagine = Image(
        str(percorso),
        width=16 * cm,
        height=9 * cm,
    )

    elementi.append(immagine)

    elementi.append(Spacer(1, 0.7 * cm))


# ==========================================================
# GENERAZIONE DEL REPORT
# ==========================================================


def genera_report(
    dataframe: pd.DataFrame,
) -> Path:
    """
    Genera il report PDF completo.

    Args:
        dataframe: riepilogo degli scenari.

    Returns:
        Percorso del PDF creato.
    """

    DOCUMENTAZIONE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    documento = SimpleDocTemplate(
        str(FILE_REPORT),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Report di monitoraggio delle prestazioni",
        author="Gabriele Piccione",
    )

    stili = getSampleStyleSheet()

    stile_titolo = ParagraphStyle(
        "TitoloPersonalizzato",
        parent=stili["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        leading=24,
        spaceAfter=18,
    )

    stile_sezione = ParagraphStyle(
        "SezionePersonalizzata",
        parent=stili["Heading2"],
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=8,
    )

    stile_testo = ParagraphStyle(
        "TestoPersonalizzato",
        parent=stili["BodyText"],
        fontSize=10.5,
        leading=15,
        spaceAfter=8,
    )

    elementi: list = []

    # Titolo principale.
    elementi.append(
        Paragraph(
            "Sistema di monitoraggio e analisi " "delle prestazioni",
            stile_titolo,
        )
    )

    elementi.append(
        Paragraph(
            "Report sperimentale generato automaticamente",
            stili["Heading3"],
        )
    )

    elementi.append(Spacer(1, 0.6 * cm))

    # Introduzione.
    elementi.append(
        Paragraph(
            "1. Obiettivo del report",
            stile_sezione,
        )
    )

    elementi.append(
        Paragraph(
            "Il presente documento riassume i risultati "
            "ottenuti durante l'esecuzione di differenti "
            "scenari di carico su una macchina virtuale "
            "Ubuntu Server. Le metriche analizzate comprendono "
            "CPU, RAM, filesystem e attività di input/output.",
            stile_testo,
        )
    )

    # Tabella.
    elementi.append(
        Paragraph(
            "2. Tabella comparativa",
            stile_sezione,
        )
    )

    elementi.append(crea_tabella_riepilogo(dataframe))

    elementi.append(PageBreak())

    # Grafici.
    elementi.append(
        Paragraph(
            "3. Grafici comparativi",
            stile_sezione,
        )
    )

    aggiungi_grafico(
        elementi,
        GRAFICO_CPU,
        "3.1 Utilizzo medio della CPU",
        stile_sezione,
    )

    aggiungi_grafico(
        elementi,
        GRAFICO_RAM,
        "3.2 Utilizzo medio della RAM",
        stile_sezione,
    )

    aggiungi_grafico(
        elementi,
        GRAFICO_DISCO,
        "3.3 Occupazione media del disco",
        stile_sezione,
    )

    elementi.append(PageBreak())

    aggiungi_grafico(
        elementi,
        GRAFICO_LETTURE,
        "3.4 Byte letti dal disco",
        stile_sezione,
    )

    aggiungi_grafico(
        elementi,
        GRAFICO_SCRITTURE,
        "3.5 Byte scritti sul disco",
        stile_sezione,
    )

    # Conclusioni.
    elementi.append(
        Paragraph(
            "4. Osservazioni conclusive",
            stile_sezione,
        )
    )

    conclusioni = genera_conclusioni(dataframe)

    for indice, conclusione in enumerate(
        conclusioni,
        start=1,
    ):
        elementi.append(
            Paragraph(
                f"{indice}. {conclusione}",
                stile_testo,
            )
        )

    documento.build(elementi)

    return FILE_REPORT


# ==========================================================
# FUNZIONE PRINCIPALE
# ==========================================================


def main() -> None:
    """
    Carica i dati e genera il report PDF.
    """

    try:
        dataframe = carica_riepilogo()

        percorso = genera_report(dataframe)

        print("Report PDF generato correttamente:")
        print(percorso)

    except (
        FileNotFoundError,
        ValueError,
        KeyError,
    ) as errore:
        print(f"\nErrore durante la generazione: {errore}")


if __name__ == "__main__":
    main()
