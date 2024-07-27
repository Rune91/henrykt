from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField, FieldList
from wtforms.validators import DataRequired, NumberRange

class NewRoundForm(FlaskForm):
    players = FieldList(SelectField("Navn", choices=[1], validators=[], coerce=int))
    throws = FieldList(IntegerField(validators=[DataRequired(), NumberRange(min=1, max=99)]))
    submit = SubmitField("Lagre runde")