from flask import session
from database import execute_select_statement, execute_non_select_statement, change_db_connection

def create_quiz(quiz_data):
    insert_query = "INSERT INTO quiz (author_id, name) VALUES (%s, %s)"
    insert_values = (session['author_id'], quiz_data['name'])
    execute_non_select_statement(insert_query, insert_values)
    select_query = "SELECT id FROM quiz WHERE name = %s"
    id = execute_select_statement(select_query, (quiz_data['name'],), num_results=1)['id']
    question_number = 1
    while str("question-" + str(question_number)) in quiz_data:
        question_data = quiz_data[str("question-" + str(question_number))]
        create_question(id, question_data)
        question_number += 1

def create_question(quiz_id, question_data):
    insert_query = "INSERT INTO question (quiz_id, question_text) VALUES (%s, %s)"
    insert_values = (quiz_id, question_data['question_text'])
    execute_non_select_statement(insert_query, insert_values)
    select_query = "SELECT id FROM question WHERE quiz_id = %s AND question_text = %s"
    id = execute_select_statement(select_query, (quiz_id, question_data['question_text']), num_results=1)['id']
    answer_number = 1
    while str("answer-" + str(answer_number)) in question_data:
        answer_data = question_data[str("answer-" + str(answer_number))]
        create_answer(id, answer_data)
        answer_number += 1

def create_answer(question_id, answer_data):
    insert_query = "INSERT INTO answer (question_id, answer_text, is_correct) VALUES (%s, %s, %s)"
    insert_values = (question_id, answer_data['answer_text'], answer_data['is_correct'])
    execute_non_select_statement(insert_query, insert_values)

def view_quiz(quiz_name):
    select_query = "SELECT * FROM quiz WHERE name = %s"
    quiz = execute_select_statement(select_query, (quiz_name,), num_results=1)
    quiz['questions'] = view_questions(quiz['id'])
    return quiz

def view_questions(quiz_id):
    select_query = "SELECT * FROM question WHERE quiz_id = %s"
    questions = execute_select_statement(select_query, (quiz_id,))
    for question in questions:
        question['answers'] = view_answers(question['id'])
    return questions

def view_answers(question_id):
    select_query = "SELECT * FROM answer WHERE question_id = %s"
    return execute_select_statement(select_query, (question_id,))