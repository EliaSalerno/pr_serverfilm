import mimetypes
import subprocess
import shutil
import threading
import time
import ctypes
from pathlib import Path
from flask import Flask, render_template, request, Response, abort, send_file

app = Flask(__name__)
BASE = Path(__file__).resolve().parent.parent
VIDEO_FOLDER = BASE / "video"
THUMBNAIL_CACHE = BASE / ".thumbnails"
STATIC_IMG = Path(__file__).resolve().parent / "static" / "img"
FFMPEG_PATH = shutil.which("ffmpeg")

DRIVE_REMOVABLE = 2

VIDEO_SOURCES = {"main": VIDEO_FOLDER}
VIDEO_SOURCES_LOCK = threading.Lock()


def get_drive_type(drive_path):
    try:
        return ctypes.windll.kernel32.GetDriveTypeW(drive_path + "\\")
    except Exception:
        return 0


def scan_devices_background():
    while True:
        try:
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            drives = []
            for letter in range(26):
                if bitmask & (1 << letter):
                    drive_path = chr(65 + letter) + ":"
                    if get_drive_type(drive_path) == DRIVE_REMOVABLE:
                        drives.append(drive_path)

            new_sources = {"main": VIDEO_FOLDER}
            for drive in drives:
                video_path = Path(f"{drive}\\video")
                if video_path.exists() and video_path.is_dir():
                    device_id = drive.replace(":", "")
                    new_sources[device_id] = video_path.resolve()

            with VIDEO_SOURCES_LOCK:
                VIDEO_SOURCES.clear()
                VIDEO_SOURCES.update(new_sources)
        except Exception:
            pass
        time.sleep(30)


scanner = threading.Thread(target=scan_devices_background, daemon=True)
scanner.start()


def get_source_id(filename):
    parts = filename.replace("\\", "/").split("/")
    with VIDEO_SOURCES_LOCK:
        if len(parts) > 1 and parts[0] in VIDEO_SOURCES:
            return parts[0]
    return "main"


def resolve_video_path(filename):
    parts = filename.replace("\\", "/").split("/")
    with VIDEO_SOURCES_LOCK:
        if len(parts) > 1 and parts[0] in VIDEO_SOURCES:
            return VIDEO_SOURCES[parts[0]] / "/".join(parts[1:])
        return VIDEO_SOURCES.get("main", VIDEO_FOLDER) / filename


def get_description(video_path, source_id="main"):
    with VIDEO_SOURCES_LOCK:
        source_path = VIDEO_SOURCES.get(source_id, VIDEO_FOLDER)
    desc_path = source_path / "etichetta" / (video_path.stem + ".txt")
    if desc_path.exists():
        return desc_path.read_text(encoding="utf-8", errors="ignore").strip()
    return ""


def get_categories():
    categories = {}
    with VIDEO_SOURCES_LOCK:
        sources = dict(VIDEO_SOURCES)

    for source_id, source_path in sources.items():
        if not source_path.exists():
            continue
        prefix = "" if source_id == "main" else f"{source_id}/"
        for entry in sorted(source_path.iterdir(), key=lambda e: e.name.lower()):
            if entry.is_dir():
                cat_name = entry.name if source_id == "main" else f"[{source_id}] {entry.name}"
                cat = {"videos": [], "subcategories": {}}
                for f in sorted(entry.iterdir(), key=lambda e: e.name.lower()):
                    if f.is_dir():
                        sub_videos = sorted(
                            ({"name": v.name, "path": f"{prefix}{entry.name}/{f.name}/{v.name}", "description": get_description(v, source_id)}
                             for v in sorted(f.iterdir(), key=lambda e: e.name.lower())
                             if v.suffix.lower() == ".mp4"),
                            key=lambda v: v["name"].lower()
                        )
                        if sub_videos:
                            cat["subcategories"][f.name] = sub_videos
                    elif f.suffix.lower() == ".mp4":
                        cat["videos"].append(
                            {"name": f.name, "path": f"{prefix}{entry.name}/{f.name}", "description": get_description(f, source_id)}
                        )
                categories[cat_name] = cat
            elif entry.suffix.lower() == ".mp4":
                cat_name = "Generale" if source_id == "main" else f"[{source_id}] Generale"
                cat = categories.setdefault(cat_name, {"videos": [], "subcategories": {}})
                cat["videos"].append({"name": entry.name, "path": f"{prefix}{entry.name}", "description": get_description(entry, source_id)})
    return categories


def total_videos(categories):
    t = 0
    for cat in categories.values():
        t += len(cat["videos"])
        for sub in cat["subcategories"].values():
            t += len(sub)
    return t


@app.route("/")
def index():
    categories = get_categories()
    return render_template("index.html", categories=categories, total_videos=total_videos(categories))


@app.route("/categoria/<category_name>")
def view_category(category_name):
    categories = get_categories()
    cat = categories.get(category_name)
    if not cat:
        abort(404)
    return render_template("category.html", category_name=category_name, category=cat, categories=categories, total_videos=total_videos(categories))


@app.route("/categoria/<category_name>/<subcategory_name>")
def view_subcategory(category_name, subcategory_name):
    categories = get_categories()
    cat = categories.get(category_name)
    if not cat:
        abort(404)
    sub = cat["subcategories"].get(subcategory_name)
    if sub is None:
        abort(404)
    return render_template("category.html", category_name=category_name, subcategory_name=subcategory_name, category={"videos": sub, "subcategories": {}}, categories=categories, total_videos=total_videos(categories))


@app.route("/thumbnail/<path:filename>")
def video_thumbnail(filename):
    filepath = resolve_video_path(filename)
    if not filepath.exists() or not filepath.is_file():
        abort(404)

    source_id = get_source_id(filename)
    fp = Path(filename)

    for candidate in [
        STATIC_IMG / fp.with_suffix(".png").name,
        STATIC_IMG / fp.with_suffix(".jpg").name,
        STATIC_IMG / f"{fp.parent.name}.png",
        STATIC_IMG / f"{fp.parent.name}.jpg",
    ]:
        if candidate.exists():
            mimetype = "image/png" if candidate.suffix == ".png" else "image/jpeg"
            return send_file(candidate, mimetype=mimetype)

    thumb_name = fp.with_suffix(".jpg")
    if source_id != "main":
        thumb_path = THUMBNAIL_CACHE / source_id / thumb_name
    else:
        thumb_path = THUMBNAIL_CACHE / thumb_name

    if thumb_path.exists():
        return send_file(thumb_path, mimetype="image/jpeg")

    if not FFMPEG_PATH:
        abort(404)

    THUMBNAIL_CACHE.mkdir(parents=True, exist_ok=True)
    thumb_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        duration_cmd = [FFMPEG_PATH, "-i", str(filepath), "-f", "null", "-"]
        result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=30)
        duration_line = [l for l in result.stderr.split("\n") if "Duration" in l]
        duration_str = duration_line[0].split("Duration: ")[1].split(",")[0] if duration_line else "60"
        parts = duration_str.split(":")
        seconds = int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        seek_time = seconds * 0.2

        subprocess.run(
            [FFMPEG_PATH, "-ss", str(seek_time), "-i", str(filepath),
             "-vframes", "1", "-q:v", "5", str(thumb_path)],
            capture_output=True, timeout=30, check=True
        )

        if thumb_path.exists():
            return send_file(thumb_path, mimetype="image/jpeg")
    except Exception:
        pass

    abort(404)


@app.route("/video/<path:filename>")
def stream_video(filename):
    filepath = resolve_video_path(filename)
    if not filepath.exists() or not filepath.is_file():
        abort(404)

    file_size = filepath.stat().st_size
    range_header = request.headers.get("Range", None)

    if range_header:
        byte1, byte2 = 0, None
        range_match = range_header.replace("bytes=", "").split("-")
        byte1 = int(range_match[0])
        if range_match[1]:
            byte2 = int(range_match[1])
        else:
            byte2 = file_size - 1

        length = byte2 - byte1 + 1

        def partial_stream():
            with open(filepath, "rb") as f:
                f.seek(byte1)
                remaining = length
                while remaining > 0:
                    chunk_size = min(8192, remaining)
                    data = f.read(chunk_size)
                    if not data:
                        break
                    remaining -= len(data)
                    yield data

        resp = Response(partial_stream(), status=206, mimetype="video/mp4")
        resp.headers.add("Content-Range", f"bytes {byte1}-{byte2}/{file_size}")
        resp.headers.add("Accept-Ranges", "bytes")
        resp.headers.add("Content-Length", str(length))
        return resp

    def full_stream():
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                yield chunk

    resp = Response(full_stream(), mimetype="video/mp4")
    resp.headers.add("Accept-Ranges", "bytes")
    resp.headers.add("Content-Length", str(file_size))
    return resp


if __name__ == "__main__":
    app.run(debug=True, port=5001)
