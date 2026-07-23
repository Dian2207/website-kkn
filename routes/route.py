from flask import Blueprint, render_template
from models import Infographics


main = Blueprint("main", __name__)


# ==========================
# HALAMAN UTAMA
# ==========================

@main.route("/")
def index():

    infographic = Infographics.query.first()

    return render_template(
        "user/index.html",
        infographic=infographic
    )


# ==========================
# PROFIL DESA
# ==========================

@main.route("/profil-desa")
def profilDesa():
    return render_template("user/profilDesa.html")


# ==========================
# PROFIL KKN
# ==========================

@main.route("/profil-kkn")
def layanan():
    return render_template("user/layanan.html")


# ==========================
# BERITA
# ==========================

@main.route("/berita")
def berita():
    return render_template("user/berita.html")


@main.route("/detail-berita/<int:id>")
def detailBerita(id):
    return render_template("user/detail_berita.html")


