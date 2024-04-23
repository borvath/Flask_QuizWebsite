from database import execute_select_statement, execute_non_select_statement

def log_login(username):
    """Inserts a row into the loginLog table to log user login times"""
    query = "SELECT id FROM user WHERE username=%s;"
    values = (username,)
    user = execute_select_statement(query, values, 1)

    if user is not None:
        query = "INSERT INTO loginLog(user_id) VALUES(%s);"
        values = (user['id'],)
        return execute_non_select_statement(query, values)
    return False
