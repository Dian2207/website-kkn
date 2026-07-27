from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    static_folder="../static/static_admin",
    static_url_path="/static_admin",
    template_folder="../templates/admin",
)

@admin_bp.route("/")
def indexAdmin():
    return render_template("dashboard_admin.html")