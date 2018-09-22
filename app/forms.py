from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField

class CSV_Form(FlaskForm):
    file = FileField('Reactor state CSV file', validators=[FileRequired('Please upload a file.')])
    submit = SubmitField('Submit')
