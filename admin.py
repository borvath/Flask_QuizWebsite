from flask import Blueprint, render_template, abort
from database import execute_select_statement
from auth import check_user_permissions

admin_bp = Blueprint('admin', __name__)


@admin_bp.route("/admin/viewusers", methods=['GET', 'POST'])
def view_users():
    """Renders page where admins can view users that exist in the database."""
    if check_user_permissions("admin"):
        query = "SELECT id, username, last_name, first_name, type FROM user;"
        result = execute_select_statement(query, None)
        headings = ["ID", "Username", "Last Name", "First Name", "Type"]
        return render_template('admin_pages/view_users.html', users=result, headings=headings)
    abort(403)


@admin_bp.route("/admin/viewlogs", methods=['GET', 'POST'])
def view_logs():
    """Renders page where admins can view security logs such as login events."""
    if check_user_permissions("admin"):
        query = ("SELECT loginLog.id, user_id, username, timestamp as logs "
                 "FROM loginLog INNER JOIN user ON loginLog.user_id=user.id ORDER BY timestamp DESC;")
        result = execute_select_statement(query, None)
        headings = ["ID", "UserID", "Username", "Login Time"]
        return render_template('admin_pages/view_logins.html', logs=result, headings=headings)
    abort(403)
