from database import execute_select_statement, execute_non_select_statement


def log_login(username) -> int:
    """Inserts a row into the login_log table to log user logins"""

    query = "SELECT id FROM user WHERE username=%s;"
    values = (username,)
    user = execute_select_statement(query, values, 1)

    if user is not None:
        query = "INSERT INTO login_log(user_id) VALUES(%s);"
        values = (user['id'],)
        return execute_non_select_statement(query, values)
    return False


def get_all_quiz_creation_times(user_info: bool = False) -> list[dict] | None:
    """Returns creation time data for all quizzes.
    If user_info is False, selected data is quiz id, name, and creation time.
    If user_info is True, selected data also includes author id and username."""

    if user_info:
        query = ("SELECT quiz.id, quiz.author_id, quiz.name, user.username, quiz.creation_time"
                 " FROM quiz INNER JOIN user WHERE quiz.author_id=user.id"
                 " ORDER BY quiz.creation_time DESC;")
    else:
        query = "SELECT quiz.id, quiz.name, quiz.creation_time FROM quiz;"
    quizzes = execute_select_statement(query)
    return quizzes


def get_quiz_creation_time(quiz_id: int, user_info: bool = False) -> dict | None:
    """Returns creation time data for a single quiz.
    If user_info is False, selected data is quiz id, name, and creation time.
    If user_info is True, selected data also includes author id and username."""

    if user_info:
        query = ("SELECT quiz.id, quiz.name, user.id, user.username, quiz.creation_time"
                 " FROM quiz INNER JOIN user WHERE quiz.id=%s AND quiz.author_id=user.id;")
    else:
        query = "SELECT quiz.id, quiz.name, quiz.creation_time FROM quiz WHERE quiz.id=%s;"
    values = (quiz_id,)
    quiz = execute_select_statement(query, values)
    return quiz
