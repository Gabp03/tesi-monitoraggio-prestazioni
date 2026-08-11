# Sistema di monitoraggio e analisi delle prestazioni

Progetto sviluppato per la tesi di laurea in Programmazione.

L’applicazione monitora una macchina Linux, esegue scenari controllati di carico, analizza le metriche raccolte e genera automaticamente file CSV, grafici comparativi e un report PDF.

## Funzionalità

- Monitoraggio di CPU, RAM, swap, disco e rete
- Raccolta delle metriche in formato CSV
- Scenario baseline senza carico artificiale
- Stress test CPU, RAM, disco e combinato
- Analisi statistica dei risultati
- Confronto automatico tra scenari
- Generazione di grafici
- Generazione automatica di un report PDF
- Interfaccia a riga di comando unificata

## Tecnologie utilizzate

- Ubuntu Server
- Python
- psutil
- pandas
- matplotlib
- ReportLab
- stress-ng
- VMware
- Visual Studio Code Remote SSH

## Struttura del progetto

```text
tesi-monitoraggio/
├── data/
├── documentazione/
├── grafici/
├── src/
│   ├── analyzer.py
│   ├── collector.py
│   ├── compare_experiments.py
│   ├── compare_graphs.py
│   ├── config.py
│   ├── experiment_runner.py
│   ├── graph_generator.py
│   ├── main.py
│   ├── monitor.py
│   ├── report_generator.py
│   ├── statistics.py
│   └── stress_manager.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Installazione

Creare e attivare l’ambiente virtuale:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Installare le dipendenze Python:

```bash
pip install -r requirements.txt
```

Installare stress-ng:

```bash
sudo apt update
sudo apt install -y stress-ng
```

## Utilizzo

Visualizzare i comandi disponibili:

```bash
python src/main.py --help
```

Eseguire un singolo scenario:

```bash
python src/main.py experiment cpu --duration 30
```

Eseguire l’intero flusso sperimentale:

```bash
python src/main.py all --duration 30
```

Il comando completo esegue:

1. baseline;
2. stress CPU;
3. stress RAM;
4. stress disco;
5. stress combinato;
6. confronto statistico;
7. generazione dei grafici;
8. generazione del report PDF.

## Output

- `data/`: metriche CSV e riepilogo degli scenari
- `grafici/`: grafici temporali e comparativi
- `documentazione/`: report PDF finale

## Scenari

- `baseline`: macchina senza carico artificiale
- `cpu`: saturazione dei core disponibili
- `ram`: allocazione intensiva della memoria
- `disco`: operazioni intensive di input/output
- `combinato`: carico simultaneo su CPU e RAM

## Autore

Gabriele Piccione