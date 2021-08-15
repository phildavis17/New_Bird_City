from typing import Iterable
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired, Optional

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    for i in range(10):
        btest = BooleanField(i, validators=[Optional()])


class TripCreationForm(FlaskForm):
    """
    This form has no inherent fields, and will get checkboxes for each 
    hotspot in the Trip being generated. 
    """
    #? What validators do I need here????
    pass

    
    