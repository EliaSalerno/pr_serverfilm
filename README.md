# Server Film

Web app Flask per navigare e riprodurre video MP4 da una cartella locale, con supporto a categorie e sottocategorie dinamiche.

## Requisiti

- Python 3.8+
- Flask
- FFmpeg (per le thumbnail dei video) — [scarica qui](https://ffmpeg.org/download.html)

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

1. **Inserisci i video** — Copia i file `.mp4` nella cartella `video/`, organizza in sottocartelle per categoria (es. `video/film/`, `video/serietv/Supergirl/`).

2. **Avvia il server**:
   ```bash
   cd new_version
   python app.py
   ```

3. **Apri il browser** all'indirizzo [http://localhost:5001](http://localhost:5001).

4. **Naviga** tra le categorie principali, seleziona una sottocategoria (es. Supergirl), clicca un video per riprodurlo.

## Struttura del progetto

```
pr_serverfilm/
├── new_version/
│   ├── app.py              # Server Flask
│   ├── templates/
│   │   ├── base.html       # Layout condiviso (nav, footer, player)
│   │   ├── index.html      # Home page con categorie
│   │   └── category.html   # Pagina dinamica per categorie/sottocategorie
│   └── stitch/             # Modelli di design di riferimento
├── video/                  # Cartella per i file .mp4
│   ├── film/
│   ├── serietv/
│   │   ├── Batwoman/
│   │   └── Supergirl/
│   └── tutorial/
├── .thumbnails/          # Cache delle thumbnail (generato automaticamente)
├── .gitignore
└── README.md
```

## Categorie e sottocategorie

Il sistema è completamente dinamico: le categorie vengono generate automaticamente dalla struttura della cartella `video/`.

- Ogni **sottocartella** di `video/` diventa una **categoria principale** (es. `film`, `serietv`, `tutorial`).
- Se una categoria contiene **sottocartelle** (es. `serietv/Batwoman/`, `serietv/Supergirl/`), queste diventano **sottocategorie** navigabili con una propria pagina.
- Le categorie con **file `.mp4` diretti** (es. `film/`, `tutorial/`) mostrano i video in griglia.
- I file `.mp4` nella radice di `video/` finiscono nella categoria "Generale".

## Thumbnail

Le thumbnail vengono generate automaticamente da FFmpeg estraendo un frame al 20% della durata di ogni video. Le immagini sono cachate nella cartella `.thumbnails/` (creata automaticamente).

Se FFmpeg non è installato, le thumbnail non vengono generate e viene mostrata un'icona come placeholder.

### Installare FFmpeg

**Windows** (con winget):
```bash
winget install FFmpeg
```

Oppure scarica l'eseguibile da [ffmpeg.org](https://ffmpeg.org/download.html) e aggiungilo al PATH.

**Linux**:
```bash
sudo apt install ffmpeg
```

**macOS**:
```bash
brew install ffmpeg
```

## Streaming

Il server supporta lo streaming con richieste HTTP Range, permettendo di saltare avanti/indietro e di riprendere la riproduzione da dove era stata interrotta.
