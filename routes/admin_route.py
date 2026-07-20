# routes/admin_route.py

from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    static_folder="../static/static_admin",
    static_url_path="/static_admin",
    template_folder="../templates/admin",
)


# ==========================
# DASHBOARD
# ==========================

@admin_bp.route("/")
def dashboard():
    return render_template("admin/dashboard.html")


# ==========================
# LOGIN
# ==========================

@admin_bp.route("/login")
def login():
    return render_template("admin/login.html")


# ==========================
# BERITA
# ==========================

@admin_bp.route("/berita")
def berita():
    return render_template("admin/berita.html")


# ==========================
# PROGRAM KERJA
# ==========================

@admin_bp.route("/program-kerja")
def programKerja():
    return render_template("admin/program_kerja.html")


# ==========================
# GALERI
# ==========================

@admin_bp.route("/galeri")
def galeri():
    return render_template("admin/galeri.html")


# ==========================
# ANGGOTA
# ==========================

@admin_bp.route("/anggota")
def anggota():
    return render_template("admin/anggota.html")


# ==========================
# LAYANAN
# ==========================

@admin_bp.route("/layanan")
def layanan():
    return render_template("admin/layanan.html")


# ==========================
# PENGADUAN
# ==========================

@admin_bp.route("/pengaduan")
def pengaduan():
    return render_template("admin/pengaduan.html")


# ==========================
# PENGATURAN WEBSITE
# ==========================

@admin_bp.route("/pengaturan")
def pengaturan():
    return render_template("admin/pengaturan.html")