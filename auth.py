from flask import session
from flask_bcrypt import Bcrypt
from database import execute_select_statement, execute_non_select_statement, change_db_connection

bcrypt = Bcrypt()


def attempt_login(data: dict) -> bool:
    if not all(i in data for i in ['username', 'password', 'type']):
        session['login_error'] = "Missing form information"
        return False
    query = "SELECT first_name, password FROM user WHERE username=%s AND type=%s;"
    values = (data['username'], data['type'])
    result = execute_select_statement(query, values, 1)
    if result is not None:
        if bcrypt.check_password_hash(result['password'], data['password']):
            session.update({"user": data["username"], "first_name": result["first_name"], "user_type": data["type"]})
            change_connected_user()
            session["login_error"] = None
            return True
        else:
            session['login_error'] = "Password not valid"
            return False
    session['login_error'] = "User not found"
    return False


def change_connected_user():
    if "user_type" in session:
        if session["user_type"] in ['student', 'teacher']:
            change_db_connection('user', 'user_password')
        elif session["user_type"] in ['admin']:
            change_db_connection('admin', 'admin_password')
    else:
        change_db_connection('unprivileged', 'unprivileged_password')


def attempt_register(data: dict) -> bool:
    if not all(i in data for i in ['first_name', 'last_name', 'username', 'password', 'type']):
        session['register_error'] = "Missing form information"
        return False
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    query = "INSERT INTO user(first_name, last_name, username, password, type) VALUES (%s, %s, %s, %s, %s)"
    values = (data['first_name'], data['last_name'], data['username'], hashed_password, data['type'])
    if execute_non_select_statement(query, values):
        session.update({"user": data["username"], "first_name": data["first_name"], "user_type": data["type"]})
        session['register_error'] = None
        return True
    else:
        session['register_error'] = "Unable to register"
        return False


def get_current_user_role() -> str:
    curr_role_dict = execute_select_statement(query="SELECT CURRENT_ROLE();", num_results=1)
    curr_role = curr_role_dict['CURRENT_ROLE()'].split('@')[0].strip('`')
    return curr_role


def check_user_permissions(permission_type: str = None) -> bool:
    change_connected_user()
    curr_role = get_current_user_role()

    if permission_type == 'user':
        return 'app_write' in curr_role or 'app_admin' in curr_role
    if permission_type == 'admin':
        return 'app_admin' in curr_role
