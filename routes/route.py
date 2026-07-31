from models import Infographics, News, Announcement
from flask import Blueprint, render_template, abort, request
from models import Infographics, News, Announcement, APBDocument

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
    page = request.args.get('page', 1, type=int)
    per_page = 5  # 1 headline + 4 small news per halaman

    # Ambil semua berita dengan pagination
    news_pagination = News.query.order_by(News.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    news_list = news_pagination.items
    total_pages = news_pagination.pages
    current_page = news_pagination.page

    # Ambil pengumuman (tidak dipaginasi)
    announcements = (
        Announcement.query
        .order_by(Announcement.created_at.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "user/berita.html",
        news=news_list,
        announcements=announcements,
        total_pages=total_pages,
        current_page=current_page
    )

@main.route("/detail-berita/<int:id>")
def detailBerita(id):
    news_item = News.query.get_or_404(id)
    return render_template("user/detail_berita.html", news=news_item)

# ==========================
# PENGUMUMAN & AGENDA (Kalender)
# ==========================
@main.route("/pengumuman")
def pengumuman():
    announcements = (
        Announcement.query
        .order_by(Announcement.created_at.desc())
        .all()
    )
    return render_template("user/pengumuman.html", announcements=announcements)

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

# ==========================
# APBDES
# ==========================

@main.route("/apbdes")
def apbdes():
    documents = APBDocument.query.order_by(APBDocument.year.desc(), APBDocument.id.desc()).all()
    return render_template(
        "user/apbdes.html",
        documents=documents
    )