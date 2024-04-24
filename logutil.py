from database import execute_select_statement, execute_non_select_statement


def log_login(username):
    """Inserts a row into the login_log table to log user logins"""
    query = "SELECT id FROM user WHERE username=%s;"
    values = (username,)
    user = execute_select_statement(query, values, 1)

    if user is not None:
        query = "INSERT INTO login_log(user_id) VALUES(%s);"
        values = (user['id'],)
        return execute_non_select_statement(query, values)
    return False


def get_all_quiz_creation_times(user_info=False):
    if user_info:
        query = ("SELECT quiz.id, quiz.author_id, quiz.name, user.username, quiz.creation_time"
                 " FROM quiz INNER JOIN user WHERE quiz.author_id=user.id"
                 " ORDER BY quiz.creation_time DESC;")
    else:
        query = "SELECT quiz.id, quiz.name, quiz.creation_time FROM quiz;"
    quizzes = execute_select_statement(query)
    return quizzes


def get_quiz_creation_time(quiz_id, user_info=False):
    if user_info:
        query = ("SELECT quiz.id, quiz.name, user.id, user.username, quiz.creation_time"
                 " FROM quiz INNER JOIN user WHERE quiz.id=%s AND quiz.author_id=user.id;")
    else:
        query = "SELECT quiz.id, quiz.name, quiz.creation_time FROM quiz WHERE quiz.id=%s;"
    values = (quiz_id,)
    quizzes = execute_select_statement(query, values)
    return quizzes
