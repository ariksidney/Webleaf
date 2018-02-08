from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class AddAuroraForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 64)])
    ip = StringField('IP Address', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()], default="16021")
    token = StringField('Token')
    submit = SubmitField('Save')
    #  TODO add ip regex
