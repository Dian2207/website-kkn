from flask import Blueprint, render_template, abort
from models import Infographics, News, Announcement

main = Blueprint("main", __name__)

# ==========================
# HALAMAN UTAMA
# ==========================
@main.route('/')
def index():
    infographic = Infographics.query.first()
    announcements = (
        Announcement.query
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )
    news = (
        News.query
        .order_by(News.published_at.desc())
        .limit(3)
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
# LAYANAN (Profil KKN)
# ==========================
@main.route("/profil-kkn")
def layanan():
    return render_template("user/layanan.html")

# ==========================
# BERITA & INFORMASI
# ==========================
@main.route("/berita")
def berita():
    # Ambil semua berita, urutkan dari terbaru
    all_news = News.query.order_by(News.published_at.desc()).all()
    announcements = (
        Announcement.query
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )
    return render_template(
        "user/berita.html",
        news=all_news,
        announcements=announcements
    )

@main.route("/detail-berita/<int:id>")
def detailBerita(id):
    news_item = News.query.get_or_404(id)
    return render_template("user/detail_berita.html", news=news_item)

# ==========================
# PENDUDUK
# ==========================
@main.route("/penduduk")
def penduduk():
    infographic = Infographics.query.first()

    return render_template(
        "user/penduduk.html",
        infographic=infographic
    )