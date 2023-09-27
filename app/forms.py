from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms.validators import InputRequired
from flask_wtf.file import FileAllowed



class ImageForm(FlaskForm):
    image = FileField(validators=[InputRequired(), FileAllowed(upload_set=['png', 'tiff', 'jpeg', 'jpg', 'dicom'], message='Tipo de arquivo não permitido.')])