from flask import Flask, render_template, request, redirect, url_for, session
from forms import LoginForm, RegisterForm
from auth import attempt_register, attempt_login
from admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = "some_key"
app.register_blueprint(admin_bp)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        logout()
    if request.method == 'GET':
        return render_template("login.html", form=LoginForm())
    else:
        if attempt_login(request.form):
            return redirect(url_for('index'))
        else:
            return render_template("login.html", form=LoginForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form=RegisterForm())
    else:
        if attempt_register(request.form):
            return redirect(url_for('index'))
        else:
            return render_template('register.html', form=RegisterForm())


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        if key != 'csrf_token':
            del session[key]
    return redirect(url_for("index"))


@app.route('/quiz-creator')
def quiz_creator():
    return render_template('createQuiz.html')


@app.route('/quizzes')
def view_quizzes(): 
    return render_template('viewQuiz.html')


if __name__ == '__main__':
    app.run(debug=True)
