# app/forms.py

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
    picture = FileField('Upload Image', validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'])])

