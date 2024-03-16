from os import environ
import mysql.connector
from mysql.connector import errorcode, connect


try:
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': f'{environ['MYSQL_PASS']}',
        'database': 'quizmaker'
    }
    db = connect(**db_config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(-1)


def execute_select(query: str, values: tuple, num_results: int = 0):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, values)
        if num_results == 0:
            results = cursor.fetchall()
        elif num_results == 1:
            results = cursor.fetchone()
        else:
            results = cursor.fetchmany(num_results)
        if cursor.fetchwarnings() is not None:
            print(cursor.fetchwarnings())
            return
    return results


def execute_insert(query, values):
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, values)
        if cursor.fetchwarnings() is not None:
            print(cursor.fetchwarnings())
            db.rollback()
            return False
        db.commit()
    return True
