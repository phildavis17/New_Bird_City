from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Optional

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    for i in range(10):
        btest = BooleanField(i, validators=[Optional()])



class TripCreationForm(FlaskForm):
    pass