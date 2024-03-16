from flask import session
from flask_bcrypt import Bcrypt
from database import execute_select, execute_insert

bcrypt = Bcrypt()


def attempt_login(data: dict) -> bool:
    if not all(i in data for i in ['username', 'password', 'type']):
        session['login_error'] = "Missing form information"
        return False
    query = "SELECT first_name, password FROM user WHERE username=%s AND type=%s;"
    values = (data['username'], data['type'])
    result = execute_select(query, values, 1)
    if result is not None:
        if bcrypt.check_password_hash(result['password'], data['password']):
            session.update({"user": data["username"], "first_name": result["first_name"], "user_type": data["type"]})
            session["login_error"] = None
            return True
        else:
            session['login_error'] = "Password not valid"
            return False
    session['login_error'] = "User not found"
    return False


def attempt_register(data: dict) -> bool:
    if not all(i in data for i in ['first_name', 'last_name', 'username', 'password', 'type']):
        session['register_error'] = "Missing form information"
        return False
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    query = "INSERT INTO user(first_name, last_name, username, password, type) VALUES (%s, %s, %s, %s, %s)"
    values = (data['first_name'], data['last_name'], data['username'], hashed_password, data['type'])
    if execute_insert(query, values):
        session.update({"user": data["username"], "first_name": data["first_name"], "user_type": data["type"]})
        session['register_error'] = None
        return True
    else:
        session['register_error'] = "Unable to register"  # Need a better way of getting an error message here
        return False
