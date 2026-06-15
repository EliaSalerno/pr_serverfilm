# KINGSTREAM

Web app Flask ispirata a Flash (DC) per navigare e riprodurre video MP4 da una cartella locale, con categorie e sottocategorie dinamiche.

## Requisiti

- Python 3.8+
- Flask
- FFmpeg (per le thumbnail) — [scarica qui](https://ffmpeg.org/download.html)

## Installazione

```bash
git clone <url>
cd pr_serverfilm

python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/macOS

pip install flask
```

## Utilizzo

1. **Inserisci i video** — Copia i file `.mp4` in `video/`, organizzati per categoria (es. `video/film/`, `video/serietv/Supergirl/`).

2. **Avvia il server** (sviluppo):
   ```bash
   cd new_version
   python app.py
   ```

3. **Avvia il server** (produzione con Waitress):
   ```bash
   pip install waitress
   cd new_version
   waitress-serve --host 0.0.0.0 --port 5001 app:app
   ```

4. Apri [http://localhost:5001](http://localhost:5001).

## Struttura del progetto

```
pr_serverfilm/
├── new_version/
│   ├── app.py                # Server Flask
│   ├── templates/
│   │   ├── base.html         # Layout (nav, footer, player)
│   │   ├── index.html        # Home page
│   │   └── category.html     # Pagina categoria/sottocategoria
│   ├── static/
│   │   └── img/              # Immagini (sfondo, thumbnail statiche)
│   └── stitch/               # Modelli di design di riferimento
├── video/                    # Cartella per i file .mp4
│   ├── film/
│   ├── serietv/
│   │   ├── Batwoman/
│   │   └── Supergirl/
│   ├── tutorial/
│   └── etichetta/            # File .txt con descrizioni (stesso nome del .mp4)
├── .thumbnails/              # Cache thumbnail (auto-generato)
├── .gitignore
└── README.md
```

## Categorie e sottocategorie

Il sistema è dinamico: le categorie nascono dalla struttura di `video/`.

- Ogni **sottocartella** di `video/` → categoria principale.
- Se una categoria contiene **sottocartelle** (es. `serietv/Supergirl/`) → sottocategorie navigabili.
- Categorie con **file `.mp4` diretti** → griglia video.
- File `.mp4` nella radice di `video/` → categoria "Generale".

## Thumbnail

Generate automaticamente da FFmpeg (frame al 20% della durata), cachate in `.thumbnails/`. Se FFmpeg è assente, viene mostrata un'icona placeholder.

```bash
# Windows
winget install FFmpeg

# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Descrizioni video

Crea un file `.txt` con lo stesso nome del `.mp4` in `video/etichetta/`:

```
video/film/Masters_Of_The_Universe_2026.mp4
video/etichetta/Masters_Of_The_Universe_2026.txt   ← descrizione
```

Il contenuto appare sotto la card (max 2 righe visibili, spazio riservato anche se assente).

**Lunghezza consigliata (in caratteri):**
- **Molto breve** (~10–30) — una riga. Ideale per genere/anno (es. `Azione 2026`).
- **Media** (~50–200) — fino a 2 righe. Adatta per un breve riassunto.
- **Lungo** (oltre 200) — troncato con puntini. Il contenuto completo rimane nel file.

## Streaming

Supporta richieste HTTP Range per saltare avanti/indietro e riprendere la riproduzione.

## Tema Flash (DC)

Il tema si ispira alla tuta di Flash: rosso (`#DC2626`) e oro (`#FBBF24`) su sfondo bordeaux scuro (`#100808`).
