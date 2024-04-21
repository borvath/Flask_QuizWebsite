from flask import Blueprint, render_template, abort
from database import execute_select_statement
from auth import check_user_permissions

admin_bp = Blueprint('admin', __name__)


# TODO: Authentication
@admin_bp.route("/viewusers", methods=['GET', 'POST'])
def view_users():
    """Renders page where admins can view users that exist in the database."""
    if check_user_permissions("admin"):
        query = "SELECT id, username, last_name, first_name, type FROM user;"
        result = execute_select_statement(query, None)
        headings = ["ID", "Username", "Last Name", "First Name", "Type"]
        return render_template('admin_pages/view_users.html', users=result, headings=headings)
    abort(403)
