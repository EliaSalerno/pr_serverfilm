import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, Response, abort

app = Flask(__name__)
BASE = Path(__file__).resolve().parent.parent
VIDEO_FOLDER = BASE / "video"

def get_categories():
    if not VIDEO_FOLDER.exists():
        return {}
    categories = {}
    for entry in sorted(VIDEO_FOLDER.iterdir(), key=lambda e: e.name.lower()):
        if entry.is_dir():
            cat = {"videos": [], "subcategories": {}}
            for f in sorted(entry.iterdir(), key=lambda e: e.name.lower()):
                if f.is_dir():
                    sub_videos = sorted(
                        ({"name": v.name, "path": f"{entry.name}/{f.name}/{v.name}"}
                         for v in sorted(f.iterdir(), key=lambda e: e.name.lower())
                         if v.suffix.lower() == ".mp4"),
                        key=lambda v: v["name"].lower()
                    )
                    if sub_videos:
                        cat["subcategories"][f.name] = sub_videos
                elif f.suffix.lower() == ".mp4":
                    cat["videos"].append(
                        {"name": f.name, "path": f"{entry.name}/{f.name}"}
                    )
            categories[entry.name] = cat
        elif entry.suffix.lower() == ".mp4":
            cat = categories.setdefault("Generale", {"videos": [], "subcategories": {}})
            cat["videos"].append({"name": entry.name, "path": entry.name})
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

@app.route("/video/<path:filename>")
def stream_video(filename):
    filepath = VIDEO_FOLDER / filename
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
    app.run(debug=True, host="0.0.0.0", port=5001)
