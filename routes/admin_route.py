from flask import Blueprint, render_template, session, redirect, url_for
from models import Infographics, News, Announcement

admin_bp = Blueprint(
    "admin_bp",
    __name__,
    static_folder="../static/static_admin",
    static_url_path="/static_admin",
    template_folder="../templates/admin",
)

@admin_bp.route("/")
def indexAdmin():
    # --- Ambil data statistik dasar ---
    total_news = News.query.count()
    total_announcements = Announcement.query.count()
    infographic = Infographics.query.first()

    # Default values
    total_population = 0
    total_family = 0
    gender_data = []
    pendidikan_data = []
    pekerjaan_list = []

    if infographic:
        total_population = infographic.total_population or 0
        total_family = infographic.total_family or 0

        # ---------- GENDER ----------
        male = infographic.male or 0
        female = infographic.female or 0
        total_gender = male + female
        if total_gender > 0:
            gender_data = [
                {'label': 'Laki-laki', 'value': round((male / total_gender) * 100, 1), 'count': male},
                {'label': 'Perempuan', 'value': round((female / total_gender) * 100, 1), 'count': female}
            ]

        # ---------- PENDIDIKAN (TOP 5) ----------
        pendidikan_fields = {
            'Belum Sekolah': infographic.belum_sekolah or 0,
            'Belum Tamat SD': infographic.belum_tamat_sd or 0,
            'Tamat SD': infographic.tamat_sd or 0,
            'Tamat SMP': infographic.tamat_smp or 0,
            'Tamat SLTA': infographic.tamat_slta or 0,
            'Diploma I/II/III': infographic.diploma_i_ii_iii or 0,
            'Sarjana S1': infographic.sarjana_s1 or 0,
            'Diploma IV/Strata I': infographic.diploma_iv_strata_i or 0,
            'Strata II': infographic.strata_ii or 0,
            'Strata III': infographic.strata_iii or 0
        }
        # Filter yang nilainya > 0
        filtered = {k: v for k, v in pendidikan_fields.items() if v > 0}
        # Urutkan dari yang terbesar
        sorted_pendidikan = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
        # Ambil 5 teratas
        top_5 = sorted_pendidikan[:5]
        remaining = sum(v for _, v in sorted_pendidikan[5:])
        # Bangun data untuk grafik
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

        # ---------- PEKERJAAN (TOP 5) ----------
        pekerjaan_fields = {
            'Belum/Tidak Bekerja': infographic.belum_tidak_bekerja or 0,
            'Mengurus Rumah Tangga': infographic.mengurus_rumah_tangga or 0,
            'Pelajar/Mahasiswa': infographic.pelajar_mahasiswa or 0,
            'Pensiunan': infographic.pensiunan or 0,
            'PNS': infographic.pns or 0,
            'Wiraswasta': infographic.wiraswasta or 0,
            'Petani/Perkebunan': infographic.petani_perkebunan or 0,
            'Peternak': infographic.peternak or 0,
            'Karyawan': infographic.karyawan or 0,
            'Buruh Pabrik': infographic.buruh_pabrik or 0,
            'Guru': infographic.guru or 0,
            'Bidan': infographic.bidan or 0,
            'Perawat': infographic.perawat or 0,
            'Pedagang': infographic.pedagang or 0
        }
        filtered_pekerjaan = {k: v for k, v in pekerjaan_fields.items() if v > 0}
        sorted_pekerjaan = sorted(filtered_pekerjaan.items(), key=lambda x: x[1], reverse=True)
        top_5_pekerjaan = sorted_pekerjaan[:5]
        remaining_pekerjaan = sum(v for _, v in sorted_pekerjaan[5:])
        # Warna untuk pie chart
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

    # Kirim semua data ke template
    return render_template(
        "dashboard_admin.html",
        total_news=total_news,
        total_announcements=total_announcements,
        total_population=total_population,
        total_family=total_family,
        gender_data=gender_data,
        pendidikan_data=pendidikan_data,
        pekerjaan_list=pekerjaan_list
    )

@admin_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))