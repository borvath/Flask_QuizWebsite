from flask import session, flash
from database import execute_select_statement, execute_non_select_statement


def create_quiz(quiz_data):
    if len(execute_select_statement("SELECT id FROM quiz WHERE name=%s", (quiz_data['quiz-title'],))) >= 1:
        flash("Quiz name already used")
        return False
    insert_query = "INSERT INTO quiz (author_id, name, description, course) VALUES (%s, %s, %s, %s);"
    
    course = quiz_data.get('course', None)
    if course:
        course = course.replace('/', '').strip() 
    insert_values = (session['user_id'], quiz_data['quiz-title'], quiz_data['quiz-description'], course)
    quiz_id = execute_non_select_statement(insert_query, insert_values)
    if quiz_id is None:
        return False
    
    i = 1
    while f"question-{i}-text" in quiz_data:
        question = {"question_text": quiz_data[f"question-{i}-text"]}
        j = 1
        while f"question-{i}-answer-{j}" in quiz_data:
            is_correct_key = f"question-{i}-choice"
            is_correct = quiz_data[is_correct_key] if is_correct_key in quiz_data else str(-1)
            if "answers" in question:
                question['answers'].append([quiz_data[f"question-{i}-answer-{j}"], is_correct])
            else:
                question['answers'] = [[quiz_data[f"question-{i}-answer-{j}"], is_correct]]
            j += 1
        create_question(quiz_id, question)
        i += 1
    return True


def create_question(quiz_id, question_data):
    insert_query = "INSERT INTO question (quiz_id, question_text) VALUES (%s, %s);"
    insert_values = (quiz_id, question_data['question_text'])
    question_id = execute_non_select_statement(insert_query, insert_values)
    for idx, answer in enumerate(question_data['answers']):
        answer_data = {"answer_text": answer[0], "is_correct": 1 if answer[1] == str(idx + 1) else 0}
        create_answer(question_id, answer_data)


def create_answer(question_id, answer_data):
    insert_query = "INSERT INTO answer (question_id, answer_text, is_correct) VALUES (%s, %s, %s);"
    insert_values = (question_id, answer_data['answer_text'], answer_data['is_correct'])
    execute_non_select_statement(insert_query, insert_values)


def get_quiz(quiz_name):
    select_query = "SELECT * FROM quiz WHERE name = %s;"
    quiz = execute_select_statement(select_query, (quiz_name,), num_results=1)
    quiz['questions'] = get_questions(quiz['id'])
    return quiz


def get_all_quizzes():
    select_query = "SELECT * FROM quiz;"
    quizzes = execute_select_statement(select_query)
    for quiz in quizzes:
        quiz['questions'] = get_questions(quiz['id'])
    return quizzes


def get_questions(quiz_id):
    select_query = "SELECT * FROM question WHERE quiz_id = %s;"
    questions = execute_select_statement(select_query, (quiz_id,))
    for question in questions:
        question['answers'] = get_answers(question['id'])
    return questions


def get_answers(question_id):
    select_query = "SELECT * FROM answer WHERE question_id = %s;"
    return execute_select_statement(select_query, (question_id,))


def grade_quiz(form_data):
    quiz = get_quiz_by_name(form_data['quiz_name'])
    questions = quiz['questions']
    num_correct = 0
    for i, question in enumerate(questions):
        answers = question['answers']
        for j, answer in enumerate(answers):
            if answer['is_correct'] == 1 and int(form_data[f'question_{i}']) == j:
                num_correct += 1
    flash(f"Your grade for this attempt is: {num_correct}/{len(questions)}")


def get_quiz_names():
    return execute_select_statement("SELECT name FROM quiz;")


def get_courses():
    return execute_select_statement("SELECT DISTINCT course FROM quiz;")


def get_quizzes_by_course(course):
    select_query = "SELECT * FROM quiz WHERE course = %s;"
    quizzes = execute_select_statement(select_query, (course,))
    for quiz in quizzes:
        quiz['questions'] = get_questions(quiz['id'])
    return quizzes


def get_quiz_by_name(quiz_name):
    select_query = "SELECT * FROM quiz WHERE name = %s;"
    quiz = execute_select_statement(select_query, (quiz_name,), num_results=1)
    if quiz:
        quiz['questions'] = get_questions(quiz['id'])
    return quiz
