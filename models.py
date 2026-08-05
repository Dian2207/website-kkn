import datetime

from extensions import db

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='admin')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# ---------- INFOGRAPHICS ----------
class Infographics(db.Model):
    __tablename__ = "infographics"

    id = db.Column(db.Integer, primary_key=True)
    total_population = db.Column(db.Integer, default=0)
    total_family = db.Column(db.Integer, default=0)
    male = db.Column(db.Integer, default=0)
    female = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Pendidikan
    belum_sekolah = db.Column(db.Integer, default=0)
    belum_tamat_sd = db.Column(db.Integer, default=0)
    tamat_sd = db.Column(db.Integer, default=0)
    tamat_smp = db.Column(db.Integer, default=0)
    tamat_slta = db.Column(db.Integer, default=0)
    diploma_i_ii_iii = db.Column(db.Integer, default=0)
    sarjana_s1 = db.Column(db.Integer, default=0)
    diploma_iv_strata_i = db.Column(db.Integer, default=0)
    strata_ii = db.Column(db.Integer, default=0)
    strata_iii = db.Column(db.Integer, default=0)
    
    # Pekerjaan
    belum_tidak_bekerja = db.Column(db.Integer, default=0)
    mengurus_rumah_tangga = db.Column(db.Integer, default=0)
    pelajar_mahasiswa = db.Column(db.Integer, default=0)
    pensiunan = db.Column(db.Integer, default=0)
    pns = db.Column(db.Integer, default=0)
    wiraswasta = db.Column(db.Integer, default=0)
    petani_perkebunan = db.Column(db.Integer, default=0)
    peternak = db.Column(db.Integer, default=0)
    karyawan = db.Column(db.Integer, default=0)
    buruh_pabrik = db.Column(db.Integer, default=0)
    guru = db.Column(db.Integer, default=0)
    bidan = db.Column(db.Integer, default=0)
    perawat = db.Column(db.Integer, default=0)
    pedagang = db.Column(db.Integer, default=0)

# ---------- NEWS ----------
class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    slug = db.Column(db.String(255), nullable=False)

    content = db.Column(db.Text, nullable=False)

    thumbnail = db.Column(db.String(255))

    published_at = db.Column(db.DateTime)

    created_at = db.Column(
        db.DateTime,
    )

    updated_at = db.Column(
        db.DateTime,
    )

    status = db.Column(db.String(20))

# ---------- ANNOUNCEMENT ----------
class Announcement(db.Model):
    __tablename__ = "announcement"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    event_date = db.Column(db.DateTime)

    location = db.Column(db.String(255))

    created_at = db.Column(db.DateTime)

    type = db.Column(db.String(100))

# ---------- APBDES DOCUMENTS ----------
class APBDocument(db.Model):
    __tablename__ = "apb_documents"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.String(50))
    year = db.Column(db.Integer, default=2026)
    category = db.Column(db.String(50), default='current')  # 'current' atau 'arsip'
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

# ---------- BANSOS ----------
class Bansos(db.Model):
    __tablename__ = "bansos"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    file_name = db.Column(db.String(255))          # PDF file
    image_name = db.Column(db.String(255))         # Foto/gambar
    year = db.Column(db.Integer, default=2026)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())