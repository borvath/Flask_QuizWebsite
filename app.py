from flask import Flask, render_template, request, redirect, url_for, session, abort
from forms import LoginForm, RegisterForm
from auth import attempt_register, attempt_login, check_user_permissions
from admin import admin_bp
from database import execute_select_statement, execute_non_select_statement, change_db_connection
from quiz import view_questions

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


@app.route('/quizzes', methods=['GET'])
@app.route('/quizzes/<quiz_id>', methods=['GET'])
def view_quizzes(quiz_id=None): 
    if quiz_id is None:
        # Fetch all quizzes
        select_query = "SELECT * FROM quiz"
        quizzes = execute_select_statement(select_query)
        for quiz in quizzes:
            quiz['questions'] = view_questions(quiz['id'])
        return render_template('viewQuiz.html', quizzes=quizzes)
    else:
        # Fetch the quiz with the provided quiz_id
        select_query = "SELECT * FROM quiz WHERE id = %s"
        quiz = execute_select_statement(select_query, (quiz_id,), num_results=1)
        quiz['questions'] = view_questions(quiz['id'])
        return render_template('viewQuiz.html', quiz=quiz)

@app.route('/rateQuiz')
def viewRatings():
    return render_template('ratings.html')


@app.route('/quiz')
def take_quiz():
    return render_template('takeQuiz.html')

classes = [
    {"name": "COP 3363 Introduction to C++", "link": "cop3363"},
    {"name": "COP 3330 Data Structures, Algorithms, and Generic Programming I", "link": "cop3330"},
    {"name": "CDA 3100 Computer Organization I", "link": "cda3100"},
    {"name": "CEN 4020 Software Engineering I", "link": "cen4020"},
    {"name": "CEN 4090L Software Engineering Capstone", "link": "cen4090l"},
    {"name": "CIS 3250 Ethics in Computer Science", "link": "cis3250"},
    {"name": "COP 4610 Operating Systems & Concurrent Programming", "link": "cop4610"},
    {"name": "COP 4530 Data Structures, Algorithms, and Generic Programming II", "link": "cop4530"},
    {"name": "COP 4521 Secure Parallel & Distributed Programming w/ Python", "link": "cop4521"},
    {"name": "COT 4420 Theory of Computation", "link": "cot4420"}
]

@app.route('/class')
def show_classes():
    return render_template('ViewClasses.html', classes=classes)

@app.route('/class/<class_name>')
def class_details(class_name):
    class_data = next((item for item in classes if item["link"] == class_name), None)
    if class_data:
        return render_template('class_details.html', class_name=class_data["name"])
    else:
        return "Class not found", 404


if __name__ == '__main__':
    app.run(debug=True)
