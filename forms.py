from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

PASSWORD_MIN_SIZE = 6
PASSWORD_MAX_SIZE = 71

USERNAME_MIN_SIZE = 6
USERNAME_MAX_SIZE = 100

FIRST_NAME_MAX_SIZE = 100
LAST_NAME_MAX_SIZE = 100


class RegisterForm(FlaskForm):
    type = SelectField(
        label='type',
        validators=[InputRequired()],
        choices=[('student', 'student'), ('admin', 'admin')]
    )
    first_name = StringField(
        label='first_name',
        validators=[InputRequired(), Length(min=1, max=FIRST_NAME_MAX_SIZE)],
        render_kw={"placeholder": "John"}
    )
    last_name = StringField(
        label='last_name',
        validators=[InputRequired(), Length(min=1, max=LAST_NAME_MAX_SIZE)],
        render_kw={"placeholder": "Smith"}
    )
    username = StringField(
        label='username',
        validators=[InputRequired(), Length(min=USERNAME_MIN_SIZE, max=USERNAME_MAX_SIZE)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        label='password',
        validators=[InputRequired(), Length(min=PASSWORD_MIN_SIZE, max=PASSWORD_MAX_SIZE)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    type = SelectField(
        label='type',
        validators=[InputRequired()],
        choices=[('student', 'student'), ('admin', 'admin')]
    )
    username = StringField(
        label='username',
        validators=[InputRequired(), Length(min=USERNAME_MIN_SIZE, max=USERNAME_MAX_SIZE)],
        render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        label="password",
        validators=[InputRequired(), Length(min=PASSWORD_MIN_SIZE, max=PASSWORD_MAX_SIZE)],
        render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("Login")
