from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileAllowed, FileField, FileRequired

class PhotoForm(FlaskForm):
    photo = FileField(validators=[
        FileRequired(),
        FileAllowed(["jpg", "png"], "Images only! Please upload in PNG or JPG format.")
    ])

    submit = SubmitField("Print!")
