# routes/route.py

from flask import Blueprint, render_template

main = Blueprint("main", __name__)


# ==========================
# HALAMAN UTAMA
# ==========================

@main.route("/")
def home():
    return render_template("user/index.html")


# ==========================
# PROFIL DESA
# ==========================

@main.route("/profil-desa")
def profilDesa():
    return render_template("user/profil_desa.html")


# ==========================
# PROFIL KKN
# ==========================

@main.route("/profil-kkn")
def profilKKN():
    return render_template("user/profil_kkn.html")


# ==========================
# BERITA
# ==========================

@main.route("/berita")
def berita():
    return render_template("user/berita.html")


@main.route("/detail-berita/<int:id>")
def detailBerita(id):
    return render_template("user/detail_berita.html")


# ==========================
# PROGRAM KERJA
# ==========================

@main.route("/program-kerja")
def programKerja():
    return render_template("user/program_kerja.html")


# ==========================
# GALERI
# ==========================

@main.route("/galeri")
def galeri():
    return render_template("user/galeri.html")


# ==========================
# ANGGOTA KKN
# ==========================

@main.route("/anggota")
def anggota():
    return render_template("user/anggota.html")


# ==========================
# LAYANAN INFORMASI PUBLIK
# ==========================

@main.route("/layanan")
def layanan():
    return render_template("user/layanan.html")


# ==========================
# PENGADUAN
# ==========================

@main.route("/pengaduan")
def pengaduan():
    return render_template("user/pengaduan.html")


# ==========================
# KONTAK
# ==========================

@main.route("/kontak")
def kontak():
    return render_template("user/kontak.html")