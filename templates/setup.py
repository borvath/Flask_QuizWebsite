from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


app = Flask(__name__)

app.config['SECRET_KEY'] = 'Hey'


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField('Password',validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username",validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password",validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route('/')
def login_home():
    return render_template("home.html")


@app.route('/StudentHome')
def Students():
    return render_template("StudentHome.html")

@app.route('/InstructorHome')
def Instructors():
    return render_template("InstructorHome.html")

@app.route('/loginStu', methods=['GET', 'POST'])
def loginStudents():
    form = LoginForm()
    return render_template("loginStu.html", title = 'Login',form=form)




@app.route('/loginInstruc')
def loginInstructor():
    form = LoginForm()
    return render_template('loginInstruc.html', form=form)


@app.route('/registerStudents', methods=['GET', 'POST'])
def RegisterStudents():
    form = RegisterForm()
    return render_template('registerStudents.html', form=form)



@app.route('/registerInstructor')
def RegisterInstructor():
    form = RegisterForm()
    return render_template('registerInstructor.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
