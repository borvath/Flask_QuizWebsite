from flask import Flask, render_template, request, redirect, url_for, session, abort
from forms import LoginForm, RegisterForm
from auth import attempt_register, attempt_login, check_user_permissions
from admin import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = "some_key"
app.register_blueprint(admin_bp)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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
    if check_user_permissions("user"):
        return render_template('createQuiz.html')
    abort(403)


@app.route('/quizzes')
def view_quizzes(): 
    return render_template('viewQuiz.html')

@app.route('/rateQuiz')
def viewRatings():
    return render_template('ratings.html')


@app.route('/quiz')
def take_quiz():
    return render_template('takeQuiz.html')

@app.route('/class')
def showClasses():
    return render_template('classes.html')

if __name__ == '__main__':
    app.run(debug=True)
