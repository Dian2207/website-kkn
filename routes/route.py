from flask import Blueprint, render_template
from models import Infographics, News, Announcement

main = Blueprint("main", __name__)

# ==========================
# HALAMAN UTAMA
# ==========================
@main.route('/')
def index():

    infographic = Infographics.query.first()

    news = (
        News.query
        .order_by(News.published_at.desc())
        .limit(2)
        .all()
    )

    announcements = (
        Announcement.query
        .filter_by(type="Pengumuman")
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "user/index.html",
        infographic=infographic,
        news=news,
        announcements=announcements
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

@main.route("/penduduk")
def penduduk():
    return render_template("user/penduduk.html")


@main.route("/detail-berita")
def detailBerita():
    return render_template("user/detail_berita.html")


