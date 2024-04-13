from mysql.connector import Error as MySql_ERROR, errorcode, connect
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract


def change_db_connection(user, password) -> None:
    global db
    db = connect_to_database(user, password)


def connect_to_database(user, password) -> PooledMySQLConnection | MySQLConnectionAbstract:
    try:
        db_config = {'host': 'localhost', 'user': user, 'password': password, 'database': 'quizmaker'}
        return connect(**db_config)

    except MySql_ERROR as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    exit(-1)


def execute_select_statement(query: str, values: tuple = None, num_results: int = 0) -> dict | list[dict] | None:
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


def execute_non_select_statement(query, values) -> bool:
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(query, values)
        if cursor.fetchwarnings() is not None:
            print(cursor.fetchwarnings())
            db.rollback()
            return False
        db.commit()
    return True


db = connect_to_database('unprivileged', 'unprivileged_password')
