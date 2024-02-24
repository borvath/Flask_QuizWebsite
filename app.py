from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'QuizMaker'

mysql = MySQL(app)


@app.route('/')
def index():
    """
    - Should redirect user to login page if not logged in
    - If logged in should direct user to home page 'index.html'
    """
    return render_template('index.html')
