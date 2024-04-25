from flask import Blueprint, render_template, abort, request, redirect
from database import execute_select_statement, execute_non_select_statement
from auth import check_user_permissions
from logutil import get_all_quiz_creation_times

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin/view-users", methods=['GET', 'POST'])
def view_users():
    """Renders page where admins can view and manage users that exist in the database."""
    if check_user_permissions("admin"):
        if request.method == "GET":
            query = "SELECT id, username, last_name, first_name, type FROM user;"
            result = execute_select_statement(query, None)
            headings = ["ID", "Username", "Last Name", "First Name", "Type"]
            return render_template('admin_pages/view_users.html', users=result, headings=headings)

        # Request to delete a user.
        # Source of request is expected to be a button with the name 'user-delete'.
        if request.method == "POST" and request.form.get('user-delete', None):
            query = "DELETE FROM user WHERE id = %s"
            values = (request.form.get('user-delete'),)
            execute_non_select_statement(query, values)
            return redirect(request.url)

        # Request to update a user.
        # Source of request is expected to be a form with an input with the name 'update-userid'
        # Expects the following field names: update-username, update-firstname, update-lastname, and update-userid.
        elif request.method == "POST" and request.form.get('update-userid', None):
            query = ("UPDATE user SET "
                     "username = %s, first_name = %s, last_name = %s "
                     "WHERE id=%s;")
            values = (request.form['update-username'],
                      request.form['update-firstname'], request.form['update-lastname'],
                      request.form['update-userid'])
            execute_non_select_statement(query, values)
            return redirect(request.url)
        abort(500)
    abort(403)


@admin_bp.route("/admin/view-login-logs", methods=['GET', 'POST'])
def view_login_logs():
    """Renders page where admins can view login events."""
    if check_user_permissions("admin"):
        query = ("SELECT login_log.id, user_id, username, timestamp as logs "
                 "FROM login_log INNER JOIN user ON login_log.user_id=user.id ORDER BY timestamp DESC;")
        result = execute_select_statement(query, None)
        headings = ["ID", "UserID", "Username", "Login Time"]
        return render_template('admin_pages/view_login_logs.html', logs=result, headings=headings)
    abort(403)


@admin_bp.route("/admin/view-quiz-logs", methods=['GET', 'POST'])
def view_quiz_logs():
    """Renders page where admins can view quiz creation events."""
    if check_user_permissions("admin"):
        result = get_all_quiz_creation_times(True)
        headings = ["QuizID", "UserID", "Quiz Name", "Username", "Creation Time"]
        return render_template('admin_pages/view_quiz_logs.html', logs=result, headings=headings)
    abort(403)
