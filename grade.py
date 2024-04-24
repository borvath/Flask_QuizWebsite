from database import execute_select_statement, execute_non_select_statement


def get_grade(quiz_id, student_id):
    query = "SELECT score FROM grade WHERE quiz_id=%s AND user_id=student_id"
    values = (quiz_id, student_id)
    result = execute_select_statement(query, values, 1)
    return result


def get_all_grades(quiz_id):
    query = ("SELECT user.first_name, user.last_name, grade.score "
             "FROM grade INNER JOIN user ON grade.quiz_id=%s AND grade.user_id=user.id "
             "ORDER BY grade.score")
    values = (quiz_id,)
    result = execute_select_statement(query, values)
    return result


def insert_grade(quiz_id, student_id, score):
    query = "INSERT INTO grade (quiz_id, user_id, score) VALUES (%s, %s, %s)"
    values = (quiz_id, student_id, score)
    execute_non_select_statement(query, values)
