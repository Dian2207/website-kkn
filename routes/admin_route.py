from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models import Infographics, News, Announcement, User, db
from sqlalchemy import or_, and_
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import check_password_hash
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

        # Cari user berdasarkan username atau email
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

# ===== DASHBOARD ADMIN (diproteksi) =====
@admin_bp.route("/")
@login_required
def indexAdmin():
    # --- Ambil parameter filter dari URL ---
    search_news = request.args.get('search_news', '')
    search_announce = request.args.get('search_announce', '')
    filter_date_news = request.args.get('filter_date_news', 'all')
    filter_status_news = request.args.get('filter_status_news', 'all')
    filter_date_announce = request.args.get('filter_date_announce', 'all')
    filter_status_announce = request.args.get('filter_status_announce', 'all')

    page_news = request.args.get('page_news', 1, type=int)
    page_announce = request.args.get('page_announce', 1, type=int)
    per_page = 5

    # ========== BERITA ==========
    news_query = News.query
    if search_news:
        news_query = news_query.filter(News.title.like(f'%{search_news}%'))

    # Filter tanggal berdasarkan published_at
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

    # Filter status (gunakan published_at != null sebagai 'published')
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

    # ========== PENGUMUMAN ==========
    announce_query = Announcement.query
    if search_announce:
        announce_query = announce_query.filter(Announcement.title.like(f'%{search_announce}%'))

    # Filter tanggal berdasarkan event_date
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

    # Filter status (tipe: agenda atau pengumuman)
    if filter_status_announce != 'all':
        announce_query = announce_query.filter(Announcement.type == filter_status_announce)

    total_announcements = announce_query.count()
    announce_pagination = announce_query.order_by(Announcement.created_at.desc()).paginate(
        page=page_announce, per_page=per_page, error_out=False
    )
    announce_items = announce_pagination.items
    announce_total_pages = announce_pagination.pages
    announce_current_page = announce_pagination.page

    # ========== DATA INFOGRAPHICS ==========
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
                {'label': 'Laki-laki', 'value': round((male / total_gender) * 100, 1), 'count': male},
                {'label': 'Perempuan', 'value': round((female / total_gender) * 100, 1), 'count': female}
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
        colors = ['#2E7D32', '#835400', '#0054A7', '#E2A500', '#D62828', '#888888']
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
                'color': '#CCCCCC',
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
@admin_bp.route("/berita/tambah")
def tambah_berita():
    return render_template("tambah_berita.html")

# ==========================
# SIMPAN BERITA
# ==========================
@admin_bp.route("/berita/simpan", methods=["POST"])
def simpan_berita():

    judul = request.form.get("judul")
    slug = request.form.get("slug")
    ringkasan = request.form.get("ringkasan")
    content = request.form.get("content")
    tanggal = request.form.get("tanggal")
    status = request.form.get("status")

    thumbnail = request.files.get("thumbnail")

    nama_file = None

    if thumbnail:
        nama_file = secure_filename(thumbnail.filename)

        folder = os.path.join(
            admin_bp.root_path,
            "../static/uploads/news"
        )

        os.makedirs(folder, exist_ok=True)

        thumbnail.save(
            os.path.join(folder, nama_file)
        )

    berita = News(
        title=judul,
        slug=slug,
        summary=ringkasan,
        content=content,
        thumbnail=nama_file,
        publish_date=datetime.strptime(
            tanggal,
            "%Y-%m-%d"
        ),
        status=status
    )

    db.session.add(berita)
    db.session.commit()

    flash("Berita berhasil ditambahkan.")

    return redirect(url_for("admin_bp.indexAdmin"))

@admin_bp.route('/tambah-pengumuman', methods=['GET'])
@login_required
def tambah_pengumuman():
    return render_template('admin/tambah_pengumuman.html')

@admin_bp.route('/simpan-pengumuman', methods=['POST'])
@login_required
def simpan_pengumuman():
    from datetime import datetime
    judul = request.form.get('judul')
    jenis = request.form.get('jenis')
    lokasi = request.form.get('lokasi')
    deskripsi = request.form.get('deskripsi')
    tanggal = request.form.get('tanggal')
    waktu = request.form.get('waktu')
    
    event_date = None
    if tanggal and waktu:
        event_date = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M")
    
    pengumuman = Announcement(
        title=judul,
        type=jenis,
        location=lokasi,
        description=deskripsi,
        event_date=event_date,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.session.add(pengumuman)
    db.session.commit()
    flash('Pengumuman berhasil ditambahkan!', 'success')
    return redirect(url_for('admin_bp.indexAdmin'))

# ===== DETAIL PENGUMUMAN =====
@admin_bp.route('/pengumuman/detail/<int:id>', methods=['GET'])
@login_required
def detail_pengumuman(id):
    pengumuman = Announcement.query.get_or_404(id)
    return render_template('admin/detail_pengumuman.html', pengumuman=pengumuman)

# ===== UPDATE PENGUMUMAN =====
@admin_bp.route('/pengumuman/update/<int:id>', methods=['POST'])
@login_required
def update_pengumuman(id):
    pengumuman = Announcement.query.get_or_404(id)
    
    pengumuman.title = request.form.get('judul')
    pengumuman.type = request.form.get('jenis')
    pengumuman.location = request.form.get('lokasi')
    pengumuman.description = request.form.get('deskripsi')
    
    tanggal = request.form.get('tanggal')
    waktu = request.form.get('waktu')
    
    if tanggal and waktu:
        try:
            pengumuman.event_date = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M")
        except ValueError:
            pass  # biarkan kosong jika format salah
    
    db.session.commit()
    flash('Pengumuman berhasil diperbarui!', 'success')
    return redirect(url_for('admin_bp.detail_pengumuman', id=pengumuman.id))
