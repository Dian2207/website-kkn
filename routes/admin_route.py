from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    static_folder="../static/static_admin",
    static_url_path="/static_admin",
    template_folder="../templates/admin",
)

@admin_bp.route("/index-admin")
def indexAdmin():
    return render_template("user/index.html")