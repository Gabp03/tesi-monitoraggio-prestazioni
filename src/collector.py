"""
=============================================================
Sistema di monitoraggio e analisi delle prestazioni

Modulo:
collector.py

Descrizione:
Contiene le funzioni dedicate alla raccolta delle principali
metriche del sistema operativo.

Metriche raccolte:
- utilizzo della CPU;
- utilizzo di RAM e swap;
- occupazione del filesystem;
- operazioni di lettura e scrittura su disco;
- traffico di rete;
- data e ora della rilevazione.

Autore:
Gabriele Piccione
=============================================================
"""

from datetime import datetime
from typing import TypeAlias

import psutil

from config import SAMPLE_INTERVAL

# Il dizionario restituito contiene valori di tipi differenti:
# timestamp, percentuali e contatori cumulativi.
MetricValue: TypeAlias = datetime | float | int
MetricRecord: TypeAlias = dict[str, MetricValue]


def raccogli_metriche() -> MetricRecord:
    """
    Raccoglie una singola rilevazione delle metriche di sistema.

    La misurazione della CPU viene effettuata durante
    l'intervallo definito in config.py. Le altre metriche
    vengono acquisite immediatamente dopo il campionamento.

    Returns:
        MetricRecord: dizionario contenente timestamp,
        percentuali di utilizzo e contatori cumulativi.
    """

    # Misura l'utilizzo medio della CPU durante
    # l'intervallo di campionamento configurato.
    cpu_percentuale = psutil.cpu_percent(interval=SAMPLE_INTERVAL)

    # Informazioni sull'utilizzo della memoria RAM.
    memoria = psutil.virtual_memory()

    # Informazioni sull'utilizzo della memoria swap.
    swap = psutil.swap_memory()

    # Percentuale di spazio occupato nella partizione root.
    filesystem = psutil.disk_usage("/")

    # Contatori cumulativi delle operazioni di I/O su disco.
    disco_io = psutil.disk_io_counters()

    # Contatori cumulativi del traffico di rete.
    rete_io = psutil.net_io_counters()

    # Alcuni sistemi potrebbero non fornire i contatori
    # relativi all'I/O del disco. In tal caso vengono
    # utilizzati valori pari a zero.
    if disco_io is None:
        disco_letture = 0
        disco_scritture = 0
        disco_byte_letti = 0
        disco_byte_scritti = 0
    else:
        disco_letture = disco_io.read_count
        disco_scritture = disco_io.write_count
        disco_byte_letti = disco_io.read_bytes
        disco_byte_scritti = disco_io.write_bytes

    return {
        "timestamp": datetime.now(),
        "cpu": cpu_percentuale,
        "ram": memoria.percent,
        "swap": swap.percent,
        "disco": filesystem.percent,
        "letture_disco": disco_letture,
        "scritture_disco": disco_scritture,
        "byte_letti_disco": disco_byte_letti,
        "byte_scritti_disco": disco_byte_scritti,
        "bytes_inviati": rete_io.bytes_sent,
        "bytes_ricevuti": rete_io.bytes_recv,
    }
