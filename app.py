from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from forms import LoginForm, RegisterForm
from flask_bcrypt import Bcrypt
from os import environ

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = f'{environ['MYSQL_PASS']}'
app.config['MYSQL_DB'] = 'quizmaker'
app.config['SECRET_KEY'] = 'Hey'

mysql = MySQL(app)
bcrypt = Bcrypt(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    - Should redirect user to login page if not logged in
    - If logged in should direct user to home page 'index.html'
    """
    if 'user' in session:
        return render_template('index.html')
    else:
        return render_template('login.html', form=LoginForm())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html", title='Login', form=LoginForm())
    else:
        cursor = mysql.connect.cursor()
        cursor.execute("SELECT id, password FROM user WHERE username=%s AND type=%s;",
                       (request.form['username'], request.form['type']))
        data = cursor.fetchone()
        print(data)
        if data is None:
            session['login_error'] = "User not found"
            return render_template("login.html", title='Login', form=LoginForm())
        else:
            if bcrypt.check_password_hash(data[-1], request.form['password']):
                session['user'] = request.form['username']
                return redirect(url_for('index'))
            else:
                session['login_error'] = "Password not valid"
                return render_template("login.html", title='Login', form=LoginForm())


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', form=RegisterForm())
    else:
        conn = mysql.connect
        cursor = conn.cursor()
        form = request.form
        try:
            hashed_password = bcrypt.generate_password_hash(form['password']).decode('utf-8')
            query = "INSERT INTO user(first_name, last_name, username, password, type) VALUES (%s, %s, %s, %s, %s)"
            values = (form['first_name'], form['last_name'], form['username'], hashed_password, form['type'])
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"{type(e)}: {e}")
            session['register_error'] = e
            cursor.close()
            conn.close()
            return render_template('register.html', form=RegisterForm())
        session['user'] = request.form['username']
        return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
