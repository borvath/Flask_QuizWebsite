from flask import Blueprint, render_template, abort, request, redirect
from auth import check_user_permissions
from grade import get_all_grades

teacher_bp = Blueprint('teacher', __name__)


@teacher_bp.route("/teacher/view-grades/<quiz_id>", methods=['GET', 'POST'])
def view_grades(quiz_id):
    result = get_all_grades(quiz_id)
    headings = ["First Name", "Last Name", "Score"]
    return render_template('teacher_pages/view_grades.html', scores=result, headings=headings)
