from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FieldList
from wtforms.validators import DataRequired, NumberRange

class NewCourseForm(FlaskForm):
    name = StringField("Navn", validators=[DataRequired()])
    holes = IntegerField("Antall hull", validators=[DataRequired(), NumberRange(min=1, max=27)])
    submit = SubmitField("Legg til bane")


class EditCourseParsForm(FlaskForm):
    pars = FieldList(IntegerField(validators=[DataRequired(), NumberRange(min=1, max=27)]))
    submit = SubmitField("Lagre endringer")
