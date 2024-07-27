from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired

class NewOperatorForm(FlaskForm):
    name = StringField("Navn på operatør", validators=[DataRequired()])
    submit = SubmitField("Legg til")


class NewEventForm(FlaskForm):
    name = StringField("Navn på arrangement", validators=[DataRequired()])
    submit = SubmitField("Legg til")


class EditEventForm(FlaskForm):
    name = StringField("Navn", validators=[DataRequired()])
    submit = SubmitField("Endre")


class EditOperatorForm(FlaskForm):
    name = StringField("Navn", validators=[DataRequired()])
    submit = SubmitField("Endre")


class LoginForm(FlaskForm):
    username = StringField("Brukernavn", validators=[DataRequired()])
    password = StringField("PIN-kode", validators=[DataRequired()])
    submit = SubmitField("Logg inn")


class FeedbackOptionsForm(FlaskForm):
    event = SelectField("Event", validators=[DataRequired()], coerce=int)
    operator = SelectField("Operatør", validators=[DataRequired()], coerce=int)
    submit = SubmitField("Gå videre")
