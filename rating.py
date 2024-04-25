from flask import session
from database import execute_select_statement, execute_non_select_statement


def insert_rating(quiz_id, rating, stars):
    if len(execute_select_statement("SELECT * FROM ratings WHERE studentID=%s and quizID=%s",
                                    (session['user_id'], quiz_id))) >= 1:
        query = "UPDATE ratings SET studentRatings=%s, amountOfStars=%s WHERE studentId=%s and quizID=%s"
        values = (rating, stars, session['user_id'], quiz_id)
        execute_non_select_statement(query, values)
    else:
        insert_query = "INSERT INTO ratings (studentID, quizID, studentRatings, amountOfStars) VALUES (%s, %s, %s, %s);"
        values = (session['user_id'], quiz_id, rating, stars)
        execute_non_select_statement(insert_query, values)


def get_all_ratings():
    select_query = """
    SELECT r.studentID, r.quizID, r.studentRatings, r.amountOfStars, q.name as quiz_name, u.username as student_name
    FROM ratings r
    JOIN quiz q ON r.quizID = q.id
    JOIN user u ON r.studentID = u.id;
    """
    return execute_select_statement(select_query)


def get_ratings_by_quiz(quiz_id):
    select_query = """
    SELECT r.studentID, r.quizID, r.studentRatings, r.amountOfStars, q.name as quiz_name, u.username as student_name
    FROM ratings r
    JOIN quiz q ON r.quizID = q.id
    JOIN user u ON r.studentID = u.id
    WHERE r.quizID = %s;
    """
    return execute_select_statement(select_query, (quiz_id,))
