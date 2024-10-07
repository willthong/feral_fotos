from datetime import datetime
import os

from app import app
from app.forms import PhotoForm
from flask import redirect, render_template, url_for
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    form = PhotoForm()

    if form.validate_on_submit():
        file = form.photo.data
        filename = secure_filename(file.filename)
        extension = filename.split(".")[-1]
        filename = datetime.now().strftime("%Y-%m-%d %-H:%M-%S %f") + "." + extension
        file.save(os.path.join("uploads", filename))
        return redirect(url_for("success"))

    return render_template("index.html", form=form)


@app.route("/success")
def success():
    return render_template("success.html")
