import os
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, Response, abort

app = Flask(__name__)
VIDEO_FOLDER = Path("video")

def get_video_list():
    if not VIDEO_FOLDER.exists():
        return []
    return sorted(
        f.name for f in VIDEO_FOLDER.iterdir()
        if f.suffix.lower() == ".mp4"
    )

@app.route("/")
def index():
    videos = get_video_list()
    return render_template("index.html", videos=videos)

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
    app.run(debug=True, host="0.0.0.0", port=5000)
