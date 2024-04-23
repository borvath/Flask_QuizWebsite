from flask import Flask, render_template, request, redirect, url_for, session, abort, flash
from forms import LoginForm, RegisterForm
from auth import attempt_register, attempt_login, check_user_permissions
from admin import admin_bp
from quiz import create_quiz, get_quiz, get_all_quizzes, get_quiz_names, get_quizzes_by_course, get_quizzes_by_name

app = Flask(__name__)
app.config['SECRET_KEY'] = "some_key"
app.register_blueprint(admin_bp)

classes = [
    {"name": "COP 3363 Introduction to C++", "link": "cop3363"},
    {"name": "COP 3330 Data Structures Programming I", "link": "cop3330"},
    {"name": "CDA 3100 Computer Organization I", "link": "cda3100"},
    {"name": "CEN 4020 Software Engineering I", "link": "cen4020"},
    {"name": "CEN 4090L Software Engineering Capstone", "link": "cen4090l"},
    {"name": "CIS 3250 Ethics in Computer Science", "link": "cis3250"},
    {"name": "COP 4610 Operating Systems & Concurrent Programming", "link": "cop4610"},
    {"name": "COP 4530 Data Structures Programming II", "link": "cop4530"},
    {"name": "COP 4521 Secure Parallel & Distributed Programming w/ Python", "link": "cop4521"},
    {"name": "COT 4420 Theory of Computation", "link": "cot4420"}
]


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    all_quizzes = get_all_quizzes()
    return render_template('index.html', quizzes=all_quizzes)

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


@app.route('/quiz-creator', methods=["GET", "POST"])
def quiz_creator():
    if check_user_permissions("user"):
        if request.method == "GET":
            return render_template('createQuiz.html')
        if request.method == "POST":
            if create_quiz(request.form):
                flash("Success!")
            else:
                flash("Failure!")
            return redirect(url_for('index'))
    abort(403)


@app.route('/quizzes', methods=['GET'])
@app.route('/quizzes/<quiz_name>', methods=['GET'])
def view_quizzes(quiz_name=None):
    if quiz_name is None:
        quizzes = get_all_quizzes()
        if quizzes is None:
            flash("No quizzes found")
            return redirect(url_for('index'))
        return render_template('viewQuiz.html', quizzes=quizzes)
    else:
        quiz = get_quiz(quiz_name)
        if quiz is None:
            flash("Quiz does not exist")
            return redirect(url_for('index'))
        return render_template('viewQuiz.html', quizzes=quiz)


@app.route('/rateQuiz')
def view_ratings():
    return render_template('ratings.html')

@app.route('/take-quiz', methods=['POST'])
def take_quiz():
    return render_template('takeQuiz.html')
    if request.method == 'POST':
        quiz_name = request.form['quiz_name']
        quiz = get_quiz(quiz_name)
        return render_template('takeQuiz.html', quizzes=quiz)


@app.route('/class')
def show_classes():
    return render_template('ViewClasses.html', classes=classes)


@app.route('/<class_name>', methods=['GET'])
def class_details(class_name):
    class_data = next((item for item in classes if item["link"] == class_name), None)
    if class_data: 
        quizzes = get_quizzes_by_course(class_name)
        if quizzes:
            return render_template('class_details.html', class_name=class_data["name"], quizzes=quizzes)
    return render_template('class_details.html', class_name=class_data["name"] if class_data else None)

@app.route('/quiz/<quiz_name>', methods=['GET'])
def quiz_details(quiz_name):
    quiz = get_quizzes_by_name(quiz_name)
    if quiz:
        return render_template('quiz_details.html', quiz=quiz)
    else:
        return "Quiz not found", 404

if __name__ == '__main__':
    app.run(debug=True)
