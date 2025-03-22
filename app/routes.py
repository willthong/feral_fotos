from datetime import datetime
from functools import partial

import base64
import io
import os

from app import app
from app.forms import PhotoForm
from flask import (
    jsonify,
    redirect,
    render_template,
    url_for,
    request,
    send_file,
    after_this_request,
)
from functools import wraps
from PIL import Image, ImageOps, ImageDraw, ImageFont
from typing import Callable
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

TOP_MARGIN = 68
LEFT_MARGIN = 78
# Template should be 1748 x 1181
PHOTO_WIDTH = 1025
PHOTO_HEIGHT = 1239
PHOTO_COORDINATES = (LEFT_MARGIN, TOP_MARGIN)

queue = []
photo_available = False


def add_border(photo: Image.Image) -> Image.Image:
    photo = ImageOps.exif_transpose(photo)
    photo = photo.resize((PHOTO_WIDTH, PHOTO_HEIGHT))
    template = Image.open("photobooth-template.png")
    template.paste(photo, box=PHOTO_COORDINATES)
    template = template.convert("RGB")
    image_io = io.BytesIO()
    template.save(image_io, "JPEG", quality=100)
    image_io.seek(0)
    return image_io


def save_photo(image, filename: str, cropped=False):
    extension = filename.split(".")[-1] if "." in filename else "jpg"
    timestamp = datetime.now().strftime("%Y-%m-%d %-H:%M-%S %f")
    filename = timestamp
    if cropped:
        filename += "_cropped"
    filename += "." + extension.lower()
    image.save(os.path.join("app/uploads", filename))
    return


def require_api_key(key_type):
    def decorator(view_function):
        @wraps(view_function)
        def decorated_function(*args, **kwargs):
            api_key = app.config.get(f"{key_type}_API_KEY")
            if not api_key:
                raise Exception(f"Missing environment variable: {key_type}_API_KEY")
            provided_key = request.args.get(f"{key_type.lower()}_api_key")
            if not provided_key or provided_key != api_key:
                return jsonify({"error": "Invalid or missing API key"}), 401
            return view_function(*args, **kwargs)

        return decorated_function

    return decorator


require_read_api_key = require_api_key("READ")
require_write_api_key = require_api_key("WRITE")


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@require_write_api_key
def index():
    form = PhotoForm()

    if form.validate_on_submit():
        file = form.photo.data
        original_filename = secure_filename(file.filename)
        save_photo(file, original_filename, cropped=False)

        cropped_data = request.form.get("cropped-data")
        image_data = cropped_data.split(",")[1]
        decoded_data = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded_data))
        save_photo(image, original_filename, cropped=True)

        photo_with_border = add_border(image)
        queue.append(photo_with_border)

        return redirect(url_for("success"))

    return render_template("index.html", form=form)


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/get_photo", methods=["GET"])
@require_read_api_key
def get_image():
    if len(queue) == 0:
        photo_available = False
        return
    next_image = queue[0]

    @after_this_request
    def call_after_request(response):
        if response.status_code == 200:
            queue.pop(0)
        return response

    return send_file(next_image, mimetype="image/jpeg")


@app.route("/photo_available", methods=["GET"])
def photo_available():
    photo_available = len(queue) > 0
    return jsonify(1 if photo_available else 0)
