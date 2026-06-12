# Server Film

Web app Flask per navigare e riprodurre video MP4 da una cartella locale.

## Requisiti

- Python 3.8+
- Flask

## Installazione

```bash
# Clona il repository
git clone <url>
cd pr_serverfilm

# (Opzionale) Crea un ambiente virtuale
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/macOS

# Installa Flask
pip install flask
```

## Utilizzo

1. **Inserisci i video** — Copia i file `.mp4` nella cartella `video/`.

2. **Avvia il server**:
   ```bash
   python app.py
   ```

3. **Apri il browser** all'indirizzo [http://localhost:5000](http://localhost:5000).

4. **Seleziona un video** dalla lista a sinistra per riprodurlo.

## Struttura del progetto

```
pr_serverfilm/
├── app.py              # Server Flask
├── templates/
│   └── index.html      # Interfaccia web
├── video/              # Cartella per i file .mp4
├── .gitignore
└── README.md
```

## Streaming

Il server supporta lo streaming con richieste HTTP Range, permettendo di saltare avanti/indietro e di riprendere la riproduzione da dove era stata interrotta.
