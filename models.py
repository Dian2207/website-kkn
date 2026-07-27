from extensions import db

class Infographics(db.Model):
    __tablename__ = "infographics"

    id = db.Column(db.Integer, primary_key=True)

    # ======================
    # DEMOGRAFI
    # ======================

    total_population = db.Column(db.Integer)
    total_family = db.Column(db.Integer)

    male = db.Column(db.Integer)
    female = db.Column(db.Integer)

    # ======================
    # PENDIDIKAN
    # ======================

    belum_sekolah = db.Column(db.Integer)
    tamat_sd = db.Column(db.Integer)
    tamat_smp = db.Column(db.Integer)
    tamat_slta = db.Column(db.Integer)
    sarjana_s1 = db.Column(db.Integer)

    # ======================
    # PEKERJAAN
    # ======================

    petani_perkebunan = db.Column(db.Integer)
    wiraswasta = db.Column(db.Integer)
    buruh_pabrik = db.Column(db.Integer)
    pns = db.Column(db.Integer)
    pelajar_mahasiswa = db.Column(db.Integer)
    pedagang = db.Column(db.Integer)
    peternak = db.Column(db.Integer)
    karyawan = db.Column(db.Integer)
    guru = db.Column(db.Integer)
    bidan = db.Column(db.Integer)
    perawat = db.Column(db.Integer)

# ---------- NEWS ----------
class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    content = db.Column(db.Text, nullable=False)

    thumbnail = db.Column(db.String(255), nullable=True)

    published_at = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime)

    updated_at = db.Column(db.DateTime)

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