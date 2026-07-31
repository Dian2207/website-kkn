from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from models import Infographics, News, Announcement, User, APBDocument, db
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
import os

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    static_folder="../static/static_admin",
    static_url_path="/static_admin",
    template_folder="../templates/admin",
)

# -------- Decorator untuk proteksi route --------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Silakan login terlebih dahulu!', 'danger')
            return redirect(url_for('admin_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('admin_bp.indexAdmin'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Username dan password wajib diisi!', 'danger')
            return render_template('login.html')

        user = User.query.filter(
            (User.username == username) | (User.email == username)
        ).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login berhasil! Selamat datang Admin.', 'success')
            return redirect(url_for('admin_bp.indexAdmin'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('login.html')

@admin_bp.route('/logout')
def logout():
    session.clear()
    flash('Anda telah logout.', 'success')
    return redirect(url_for('admin_bp.login'))

# ===== DASHBOARD ADMIN =====
@admin_bp.route("/")
@login_required
def indexAdmin():
    search_news = request.args.get('search_news', '')
    search_announce = request.args.get('search_announce', '')
    filter_date_news = request.args.get('filter_date_news', 'all')
    filter_status_news = request.args.get('filter_status_news', 'all')
    filter_date_announce = request.args.get('filter_date_announce', 'all')
    filter_status_announce = request.args.get('filter_status_announce', 'all')

    page_news = request.args.get('page_news', 1, type=int)
    page_announce = request.args.get('page_announce', 1, type=int)
    page_dokumen = request.args.get('page_dokumen', 1, type=int)
    per_page = 5

    # ===== BERITA =====
    news_query = News.query
    if search_news:
        news_query = news_query.filter(News.title.like(f'%{search_news}%'))

    if filter_date_news != 'all':
        now = datetime.now()
        if filter_date_news == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            news_query = news_query.filter(News.published_at.between(start, end))
        elif filter_date_news == 'week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            news_query = news_query.filter(News.published_at >= start)
        elif filter_date_news == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            news_query = news_query.filter(News.published_at >= start)

    if filter_status_news == 'published':
        news_query = news_query.filter(News.published_at.isnot(None))
    elif filter_status_news == 'draft':
        news_query = news_query.filter(News.published_at.is_(None))

    total_news = news_query.count()
    news_pagination = news_query.order_by(News.published_at.desc()).paginate(
        page=page_news, per_page=per_page, error_out=False
    )
    news_items = news_pagination.items
    news_total_pages = news_pagination.pages
    news_current_page = news_pagination.page

    # ===== PENGUMUMAN =====
    announce_query = Announcement.query
    if search_announce:
        announce_query = announce_query.filter(Announcement.title.like(f'%{search_announce}%'))

    if filter_date_announce != 'all':
        now = datetime.now()
        if filter_date_announce == 'today':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            announce_query = announce_query.filter(Announcement.event_date.between(start, end))
        elif filter_date_announce == 'week':
            start = now - timedelta(days=now.weekday())
            start = start.replace(hour=0, minute=0, second=0, microsecond=0)
            announce_query = announce_query.filter(Announcement.event_date >= start)
        elif filter_date_announce == 'month':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            announce_query = announce_query.filter(Announcement.event_date >= start)

    if filter_status_announce != 'all':
        announce_query = announce_query.filter(Announcement.type == filter_status_announce)

    total_announcements = announce_query.count()
    announce_pagination = announce_query.order_by(Announcement.created_at.desc()).paginate(
        page=page_announce, per_page=per_page, error_out=False
    )
    announce_items = announce_pagination.items
    announce_total_pages = announce_pagination.pages
    announce_current_page = announce_pagination.page

    # ===== DOKUMEN APBDES =====
    dokumen_query = APBDocument.query
    total_dokumen = dokumen_query.count()
    dokumen_pagination = dokumen_query.order_by(
        APBDocument.year.desc(),
        APBDocument.id.desc()
    ).paginate(page=page_dokumen, per_page=per_page, error_out=False)
    dokumen_items = dokumen_pagination.items
    dokumen_total_pages = dokumen_pagination.pages
    dokumen_current_page = dokumen_pagination.page

    # ===== DATA INFOGRAPHICS =====
    infographic = Infographics.query.first()
    total_population = 0
    total_family = 0
    gender_data = []
    pendidikan_data = []
    pekerjaan_list = []

    if infographic:
        total_population = infographic.total_population or 0
        total_family = infographic.total_family or 0

        male = infographic.male or 0
        female = infographic.female or 0
        total_gender = male + female
        if total_gender > 0:
            gender_data = [
                {
                    'label': 'Laki-laki',
                    'value': round((male / total_gender) * 100, 1),
                    'count': male,
                    'color': '#72ED8B'
                },
                {
                    'label': 'Perempuan',
                    'value': round((female / total_gender) * 100, 1),
                    'count': female,
                    'color': '#FF9EA7'
                }
            ]

        pendidikan_fields = {
            'Belum Sekolah': infographic.belum_sekolah or 0,
            'Tamat SD': infographic.tamat_sd or 0,
            'Tamat SMP': infographic.tamat_smp or 0,
            'Tamat SLTA': infographic.tamat_slta or 0,
            'Sarjana S1': infographic.sarjana_s1 or 0,
            'Diploma I/II/III': infographic.diploma_i_ii_iii or 0,
            'Diploma IV/Strata I': infographic.diploma_iv_strata_i or 0,
            'Strata II': infographic.strata_ii or 0,
            'Strata III': infographic.strata_iii or 0
        }
        filtered = {k: v for k, v in pendidikan_fields.items() if v > 0}
        sorted_pendidikan = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
        top_5 = sorted_pendidikan[:5]
        remaining = sum(v for _, v in sorted_pendidikan[5:])
        for label, count in top_5:
            pendidikan_data.append({
                'label': label,
                'count': count,
                'value': round((count / total_population) * 100, 1) if total_population > 0 else 0
            })
        if remaining > 0:
            pendidikan_data.append({
                'label': 'Lainnya',
                'count': remaining,
                'value': round((remaining / total_population) * 100, 1) if total_population > 0 else 0
            })

        pekerjaan_fields = {
            'Petani/Perkebunan': infographic.petani_perkebunan or 0,
            'Peternak': infographic.peternak or 0,
            'Wiraswasta': infographic.wiraswasta or 0,
            'Pedagang': infographic.pedagang or 0,
            'Karyawan': infographic.karyawan or 0,
            'Buruh Pabrik': infographic.buruh_pabrik or 0,
            'PNS': infographic.pns or 0,
            'Guru': infographic.guru or 0,
            'Bidan': infographic.bidan or 0,
            'Perawat': infographic.perawat or 0,
            'Belum/Tidak Bekerja': infographic.belum_tidak_bekerja or 0,
            'Mengurus Rumah Tangga': infographic.mengurus_rumah_tangga or 0,
            'Pelajar/Mahasiswa': infographic.pelajar_mahasiswa or 0,
            'Pensiunan': infographic.pensiunan or 0
        }
        filtered_pekerjaan = {k: v for k, v in pekerjaan_fields.items() if v > 0}
        sorted_pekerjaan = sorted(filtered_pekerjaan.items(), key=lambda x: x[1], reverse=True)
        top_5_pekerjaan = sorted_pekerjaan[:5]
        remaining_pekerjaan = sum(v for _, v in sorted_pekerjaan[5:])
        colors = [
            '#2E7D32',  # Hijau
            '#996000',  # Coklat
            '#005EB8',  # Biru
            '#9E9E9E',  # Abu
            '#D0D0D0',  # Abu muda
        ]
        offset = 0
        for idx, (label, count) in enumerate(top_5_pekerjaan):
            percent = round((count / total_population) * 100, 1) if total_population > 0 else 0
            pekerjaan_list.append({
                'label': label,
                'value': percent,
                'color': colors[idx % len(colors)],
                'offset': offset
            })
            offset += percent
        if remaining_pekerjaan > 0:
            percent = round((remaining_pekerjaan / total_population) * 100, 1) if total_population > 0 else 0
            pekerjaan_list.append({
                'label': 'Lainnya',
                'value': percent,
                'color': '#E0E0E0',
                'offset': offset
            })

    return render_template(
        "dashboard_admin.html",
        total_news=total_news,
        total_announcements=total_announcements,
        total_population=total_population,
        total_family=total_family,
        gender_data=gender_data,
        pendidikan_data=pendidikan_data,
        pekerjaan_list=pekerjaan_list,
        news_items=news_items,
        news_total_pages=news_total_pages,
        news_current_page=news_current_page,
        announce_items=announce_items,
        announce_total_pages=announce_total_pages,
        announce_current_page=announce_current_page,
        dokumen_items=dokumen_items,
        dokumen_total_pages=dokumen_total_pages,
        dokumen_current_page=dokumen_current_page,
        total_dokumen=total_dokumen,
        search_news=search_news,
        search_announce=search_announce,
        filter_date_news=filter_date_news,
        filter_status_news=filter_status_news,
        filter_date_announce=filter_date_announce,
        filter_status_announce=filter_status_announce
    )

# ==========================
# HALAMAN FORM TAMBAH BERITA
# ==========================
@admin_bp.route("/edit/data")
def edit_data():
    data = Infographics.query.first()
    return render_template("admin/edit_data.html", data=data)

@admin_bp.route("/edit/data/update", methods=["POST"])
@login_required
def update_data():
    data = Infographics.query.first()
    if not data:
        data = Infographics()
        db.session.add(data)

    data.total_population = request.form.get("total_population", type=int)
    data.total_family = request.form.get("total_family", type=int)
    data.male = request.form.get("male", type=int)
    data.female = request.form.get("female", type=int)

    data.belum_sekolah = request.form.get("belum_sekolah", type=int)
    data.belum_tamat_sd = request.form.get("belum_tamat_sd", type=int)
    data.tamat_sd = request.form.get("tamat_sd", type=int)
    data.tamat_smp = request.form.get("tamat_smp", type=int)
    data.tamat_slta = request.form.get("tamat_slta", type=int)
    data.diploma_i_ii_iii = request.form.get("diploma", type=int)
    data.sarjana_s1 = request.form.get("sarjana", type=int)
    data.diploma_iv_strata_i = request.form.get("diploma_iv_strata_i", type=int)
    data.strata_ii = request.form.get("strata_ii", type=int)
    data.strata_iii = request.form.get("strata_iii", type=int)

    data.belum_tidak_bekerja = request.form.get("belum_tidak_bekerja", type=int)
    data.mengurus_rumah_tangga = request.form.get("mengurus_rumah_tangga", type=int)
    data.pelajar_mahasiswa = request.form.get("pelajar_mahasiswa", type=int)
    data.pensiunan = request.form.get("pensiunan", type=int)
    data.pns = request.form.get("pns", type=int)
    data.wiraswasta = request.form.get("wiraswasta", type=int)
    data.petani_perkebunan = request.form.get("petani", type=int)
    data.peternak = request.form.get("peternak", type=int)
    data.karyawan = request.form.get("karyawan", type=int)
    data.buruh_pabrik = request.form.get("buruh_pabrik", type=int)
    data.guru = request.form.get("guru", type=int)
    data.bidan = request.form.get("bidan", type=int)
    data.perawat = request.form.get("perawat", type=int)
    data.pedagang = request.form.get("pedagang", type=int)

    db.session.commit()
    flash("Data berhasil diperbarui.", "success")
    return redirect(url_for("admin_bp.edit_data"))

# ==========================
# TAMBAH BERITA
# ==========================
@admin_bp.route("/berita/tambah", methods=["GET","POST"])
def tambah_berita():
    if request.method=="POST":
        # simpan berita baru
        pass
    return render_template("admin/tambah_berita.html", berita=None, edit=False)

@admin_bp.route("/berita/edit/<int:id>", methods=["GET","POST"])
@login_required
def edit_berita(id):
    berita = News.query.get_or_404(id)
    if request.method == "POST":
        berita.title = request.form["title"]
        berita.slug = request.form["slug"]
        berita.content = request.form["content"]
        status = request.form.get("status")
        if status == "published":
            berita.published_at = datetime.now()
        else:
            berita.published_at = None
        berita.updated_at = datetime.now()
        file = request.files.get("thumbnail")
        if file and file.filename != "":
            filename = secure_filename(file.filename)
            os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            berita.thumbnail = filename
        db.session.commit()
        flash("Berita berhasil diperbarui.", "success")
        return redirect(url_for("admin_bp.indexAdmin"))
    return render_template("admin/tambah_berita.html", berita=berita, edit=True)

@admin_bp.route("/berita/hapus/<int:id>", methods=["POST"])
@login_required
def hapus_berita(id):
    berita = News.query.get_or_404(id)
    if berita.thumbnail:
        file_path = os.path.join(admin_bp.root_path, "../static/uploads/news", berita.thumbnail)
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(berita)
    db.session.commit()
    flash("Berita berhasil dihapus.", "success")
    return redirect(url_for("admin_bp.indexAdmin"))

@admin_bp.route("/berita/simpan", methods=["POST"])
@login_required
def simpan_berita():
    title = request.form.get("title")
    slug = request.form.get("slug")
    content = request.form.get("content")
    status = request.form.get("status")
    published_at = request.form.get("published_at")
    nama_file = None
    thumbnail = request.files.get("thumbnail")
    if thumbnail and thumbnail.filename != "":
        filename = secure_filename(thumbnail.filename)
        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        thumbnail.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        nama_file = filename
    sekarang = datetime.now()
    berita = News(
        title=title,
        slug=slug,
        content=content,
        thumbnail=nama_file,
        created_at=sekarang,
        updated_at=sekarang,
        status=status
    )
    if status == "published":
        if published_at:
            berita.published_at = datetime.strptime(published_at, "%Y-%m-%d")
        else:
            berita.published_at = sekarang
    else:
        berita.published_at = None
    db.session.add(berita)
    db.session.commit()
    flash("Berita berhasil ditambahkan.", "success")
    return redirect(url_for("admin_bp.indexAdmin"))

# ==========================
# PENGUMUMAN
# ==========================
@admin_bp.route('/tambah-pengumuman', methods=['GET'])
@login_required
def tambah_pengumuman():
    return render_template('admin/tambah_pengumuman.html')

@admin_bp.route("/pengumuman/hapus/<int:id>", methods=["POST"])
@login_required
def hapus_pengumuman(id):
    pengumuman = Announcement.query.get_or_404(id)
    db.session.delete(pengumuman)
    db.session.commit()
    flash("Pengumuman berhasil dihapus.", "success")
    return redirect(url_for("admin_bp.indexAdmin"))

@admin_bp.route("/pengumuman/edit/<int:id>")
@login_required
def edit_pengumuman(id):
    announcement = Announcement.query.get_or_404(id)
    return render_template("admin/tambah_pengumuman.html", announcement=announcement, edit=True)

@admin_bp.route('/simpan-pengumuman', methods=['POST'])
@login_required
def simpan_pengumuman():
    title = request.form.get("title")
    tipe = request.form.get("type")
    location = request.form.get("location")
    description = request.form.get("description")
    tanggal = request.form.get("event_date")
    waktu = request.form.get("event_time")
    event_date = None
    if tanggal and waktu:
        event_date = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M")
    announcement = Announcement(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        type=tipe,
        created_at=datetime.now()
    )
    db.session.add(announcement)
    db.session.commit()
    flash("Pengumuman berhasil ditambahkan!", "success")
    return redirect(url_for("admin_bp.indexAdmin"))

@admin_bp.route('/pengumuman/detail/<int:id>', methods=['GET'])
@login_required
def detail_pengumuman(id):
    pengumuman = Announcement.query.get_or_404(id)
    return render_template('admin/detail_pengumuman.html', pengumuman=pengumuman)

@admin_bp.route("/pengumuman/update/<int:id>", methods=["POST"])
@login_required
def update_pengumuman(id):
    announcement = Announcement.query.get_or_404(id)
    announcement.title = request.form.get("title")
    announcement.type = request.form.get("type")
    announcement.location = request.form.get("location")
    announcement.description = request.form.get("description")
    tanggal = request.form.get("event_date")
    waktu = request.form.get("event_time")
    if tanggal and waktu:
        announcement.event_date = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M")
    db.session.commit()
    flash("Pengumuman berhasil diperbarui.", "success")
    return redirect(url_for("admin_bp.indexAdmin"))

# ==========================
# KELOLA DOKUMEN APBDES
# ==========================

@admin_bp.route("/dokumen-apbdes")
@login_required
def kelola_dokumen_apbdes():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = APBDocument.query.order_by(
        APBDocument.year.desc(),
        APBDocument.id.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    dokumen = pagination.items
    total_pages = pagination.pages
    current_page = pagination.page
    return render_template(
        "admin/dokumen_apbdes.html",
        dokumen=dokumen,
        total_pages=total_pages,
        current_page=current_page
    )

@admin_bp.route("/dokumen-apbdes/tambah", methods=["GET", "POST"])
@login_required
def tambah_dokumen_apbdes():
    if request.method == "POST":
        title = request.form.get("title")
        year = request.form.get("year", type=int)
        category = request.form.get("category")
        description = request.form.get("description")
        file = request.files.get("file_pdf")

        if not title or not file or file.filename == "":
            flash("Judul dan file PDF wajib diisi!", "danger")
            return redirect(url_for("admin_bp.tambah_dokumen_apbdes"))

        file.seek(0, 2)
        size_bytes = file.tell()
        file.seek(0)
        size_mb = round(size_bytes / (1024 * 1024), 1)
        file_size = f"{size_mb} MB"

        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, "static", "uploads", "apbdes")
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, filename)
        file.save(file_path)

        doc = APBDocument(
            title=title,
            file_name=filename,
            file_size=file_size,
            year=year,
            category=category,
            description=description
        )
        db.session.add(doc)
        db.session.commit()

        flash("Dokumen APBDes berhasil ditambahkan.", "success")
        return redirect(url_for("admin_bp.kelola_dokumen_apbdes"))

    return render_template("admin/dokumen_apbdes_form.html", edit=False, doc=None)

@admin_bp.route("/dokumen-apbdes/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_dokumen_apbdes(id):
    doc = APBDocument.query.get_or_404(id)

    if request.method == "POST":
        doc.title = request.form.get("title")
        doc.year = request.form.get("year", type=int)
        doc.category = request.form.get("category")
        doc.description = request.form.get("description")

        file = request.files.get("file_pdf")
        if file and file.filename != "":
            old_path = os.path.join(current_app.root_path, "static", "uploads", "apbdes", doc.file_name)
            if os.path.exists(old_path):
                os.remove(old_path)

            filename = secure_filename(file.filename)
            upload_dir = os.path.join(current_app.root_path, "static", "uploads", "apbdes")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            file.seek(0, 2)
            size_bytes = file.tell()
            file.seek(0)
            size_mb = round(size_bytes / (1024 * 1024), 1)
            file_size = f"{size_mb} MB"

            doc.file_name = filename
            doc.file_size = file_size

        db.session.commit()
        flash("Dokumen berhasil diperbarui.", "success")
        return redirect(url_for("admin_bp.kelola_dokumen_apbdes"))

    return render_template("admin/dokumen_apbdes_form.html", edit=True, doc=doc)

@admin_bp.route("/dokumen-apbdes/hapus/<int:id>", methods=["POST"])
@login_required
def hapus_dokumen_apbdes(id):
    doc = APBDocument.query.get_or_404(id)
    file_path = os.path.join(current_app.root_path, "static", "uploads", "apbdes", doc.file_name)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.session.delete(doc)
    db.session.commit()

    flash("Dokumen berhasil dihapus.", "success")
    return redirect(url_for("admin_bp.kelola_dokumen_apbdes"))