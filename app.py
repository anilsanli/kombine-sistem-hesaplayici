from contextlib import nullcontext
from itertools import combinations
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Kombine Sistem Bahis Simülatörü",
    page_icon="🏇",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Güvenli Analitik İmport ve Kurulumu
try:
    import streamlit_analytics2 as streamlit_analytics

    analytics_pwd = st.secrets.get("ANALYTICS_PASSWORD", "")
    if analytics_pwd:
        analytics_context = streamlit_analytics.track(password=analytics_pwd)
    else:
        analytics_context = streamlit_analytics.track()
except Exception:
    analytics_context = nullcontext()

with analytics_context:
    # Modern, Net Ayrımlı & Yüksek Kontrastlı CSS
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background-color: #f1f5f9 !important;
            color: #0f172a;
        }

        /* Hero Banner */
        .hero-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            border-radius: 16px;
            padding: 24px 28px;
            color: #ffffff;
            margin-bottom: 20px;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.12);
        }
        .hero-title {
            font-size: 24px;
            font-weight: 800;
            margin: 0;
            color: #ffffff !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .hero-subtitle {
            font-size: 13.5px;
            color: #cbd5e1 !important;
            margin-top: 6px;
            margin-bottom: 0;
        }

        /* Segmented / Pill Radio Stili */
        div[data-testid="stRadio"] > div {
            background-color: #f1f5f9;
            padding: 3px;
            border-radius: 10px;
            display: flex;
            gap: 3px;
            border: 1px solid #e2e8f0;
        }
        div[data-testid="stRadio"] label {
            background: transparent;
            border-radius: 7px;
            padding: 5px 12px !important;
            margin: 0 !important;
            transition: all 0.2s ease;
            cursor: pointer;
            border: none !important;
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            background: #0f172a !important;
        }
        div[data-testid="stRadio"] label:has(input:checked) p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] input {
            display: none !important;
        }

        /* Sistem Seçimi Checkbox Rozetleri */
        .system-pill div[data-testid="stCheckbox"] {
            background: #ffffff;
            border: 1.5px solid #cbd5e1;
            border-radius: 8px;
            padding: 6px 4px;
            transition: all 0.15s ease;
            text-align: center;
        }
        .system-pill div[data-testid="stCheckbox"]:has(input:checked) {
            background: #fff1f2 !important;
            border-color: #e11d48 !important;
        }
        .system-pill div[data-testid="stCheckbox"]:has(input:checked) span {
            color: #e11d48 !important;
            font-weight: 700 !important;
        }

        /* Finansal Kokpit Çubuğu */
        .integrated-kpi-bar {
            display: flex;
            align-items: center;
            justify-content: space-around;
            background: linear-gradient(135deg, #090d16 0%, #111827 100%) !important;
            border-radius: 12px;
            padding: 16px 20px;
            margin-top: 14px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 20px -4px rgba(15, 23, 42, 0.2);
            flex-wrap: wrap;
            gap: 12px;
        }
        .kpi-segment {
            display: flex;
            flex-direction: column;
            gap: 2px;
            text-align: center;
        }
        .kpi-title {
            font-size: 11.5px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #94a3b8 !important;
        }
        .kpi-number {
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #ffffff !important;
        }
        .kpi-number.accent {
            color: #fb7185 !important;
        }
        .kpi-number.highlight {
            color: #34d399 !important;
            font-size: 23px !important;
        }
        .kpi-divider {
            width: 1px;
            height: 32px;
            background: rgba(255, 255, 255, 0.15);
        }

        /* Koşu & Bilet Kartı Konteyneri */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #ffffff;
            border-radius: 14px !important;
            border: 1px solid #e2e8f0 !important;
            box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04) !important;
            transition: all 0.2s ease-in-out;
            padding: 4px;
            margin-bottom: 8px;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #cbd5e1 !important;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.08) !important;
        }

        /* Kart Başlığı */
        .card-header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 8px;
            margin-bottom: 10px;
            border-bottom: 1.5px dashed #f1f5f9;
        }
        .race-pill {
            background: #f1f5f9;
            color: #475569 !important;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }
        .selection-title {
            font-size: 14px;
            font-weight: 800;
            color: #0f172a !important;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        /* Sekmeler (Tabs) */
        button[data-baseweb="tab"] {
            font-size: 13.5px !important;
            font-weight: 600 !important;
            padding: 8px 16px !important;
            border-radius: 8px 8px 0 0 !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #e11d48 !important;
            border-bottom-color: #e11d48 !important;
        }

        /* At & Bilet Rozet Stilleri */
        .chip-at-won {
            background: #dcfce7 !important;
            border: 1px solid #86efac !important;
            color: #14532d !important;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 2px;
        }
        .chip-at-lost {
            background: #fee2e2 !important;
            border: 1px solid #fca5a5 !important;
            color: #7f1d1d !important;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 2px;
            text-decoration: line-through;
            opacity: 0.85;
        }
        .chip-at-pending {
            background: #fef9c3 !important;
            border: 1px solid #fde047 !important;
            color: #713f12 !important;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 2px;
        }
        .chip-at-refund {
            background: #f1f5f9 !important;
            border: 1px solid #cbd5e1 !important;
            color: #475569 !important;
            border-radius: 6px;
            padding: 4px 8px;
            font-size: 12px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 4px;
            margin: 2px;
        }

        .slip-badge-won {
            background: #dcfce7;
            color: #15803d;
            font-weight: 800;
            font-size: 11.5px;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid #86efac;
        }
        .slip-badge-pending {
            background: #fef9c3;
            color: #854d0e;
            font-weight: 800;
            font-size: 11.5px;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid #fef08a;
        }
        .slip-badge-lost {
            background: #fee2e2;
            color: #b91c1c;
            font-weight: 800;
            font-size: 11.5px;
            padding: 3px 10px;
            border-radius: 9999px;
            border: 1px solid #fca5a5;
        }

        /* Modern Tablo Formatı */
        .table-responsive-wrapper {
            width: 100%;
            overflow-x: auto;
            display: flex;
            justify-content: flex-start;
            margin-top: 10px;
        }
        .modern-table-container {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            overflow-y: auto;
            max-height: 440px;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.03);
            display: inline-block;
            min-width: 650px;
            width: 100%;
        }
        .modern-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }
        .modern-table th {
            background: #f8fafc;
            color: #64748b;
            font-weight: 700;
            font-size: 11.5px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 12px 16px;
            border-bottom: 1.5px solid #e2e8f0;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .modern-table td {
            padding: 11px 16px;
            border-bottom: 1px solid #e2e8f0;
            color: #1e293b;
            vertical-align: middle;
        }

        .modern-table tbody tr.row-won {
            background-color: #ecfdf5 !important;
        }
        .modern-table tbody tr.row-won:hover {
            background-color: #d1fae5 !important;
        }
        .modern-table tbody tr.row-pending {
            background-color: #ffffff !important;
        }
        .modern-table tbody tr.row-pending:hover {
            background-color: #f8fafc !important;
        }
        .modern-table tbody tr.row-lost {
            background-color: #fff1f2 !important;
            opacity: 0.85;
        }
        .modern-table tbody tr.row-lost:hover {
            background-color: #ffe4e6 !important;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 700;
        }
        .status-badge.won {
            background: #dcfce7;
            color: #15803d;
            border: 1px solid #86efac;
        }
        .status-badge.pending {
            background: #fef9c3;
            color: #854d0e;
            border: 1px solid #fef08a;
        }
        .status-badge.lost {
            background: #fee2e2;
            color: #b91c1c;
            border: 1px solid #fca5a5;
        }
        .payout-val {
            font-weight: 800;
            color: #0f172a;
        }
        .payout-val.won {
            color: #16a34a;
        }

        /* Form Elemanları */
        div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #e11d48 !important;
            background-color: #ffffff !important;
            box-shadow: 0 0 0 3px rgba(225, 29, 72, 0.12) !important;
        }
        div[data-baseweb="select"] > div {
            background-color: #f8fafc !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }

        /* Expander */
        div[data-testid="stExpander"] {
            background: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            margin-top: 8px !important;
        }
        div[data-testid="stExpander"] summary {
            font-size: 12px !important;
            font-weight: 600 !important;
            color: #64748b !important;
        }

        /* Butonlar */
        div.stButton > button {
            background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(225, 29, 72, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(225, 29, 72, 0.3) !important;
        }

        /* İpucu Banner */
        .helper-banner {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #3b82f6;
            border-radius: 10px;
            padding: 10px 16px;
            margin-bottom: 16px;
            font-size: 13px;
            color: #1e293b;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }

        /* İkramiye Özet Hero Paneli */
        .payout-hero {
            background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #1e293b 100%);
            border-radius: 18px;
            padding: 24px 28px;
            margin-top: 28px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.25);
        }
        .payout-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
            gap: 16px;
            align-items: stretch;
        }
        .payout-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 18px 20px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            text-align: center;
            transition: all 0.2s ease;
        }
        .payout-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.12);
        }
        .payout-title {
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .payout-amount {
            font-size: 30px;
            font-weight: 800;
            margin: 0;
            line-height: 1.1;
        }

        /* Yasal Uyarı Kutusu */
        .legal-box {
            background-color: #fffbeb;
            border: 1px solid #fef3c7;
            border-left: 5px solid #f59e0b;
            padding: 16px 20px;
            border-radius: 12px;
            margin-top: 28px;
            margin-bottom: 15px;
            box-shadow: 0 2px 8px rgba(245, 158, 11, 0.05);
        }
        .legal-title {
            margin: 0;
            font-size: 13.5px;
            color: #b45309 !important;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .legal-text {
            margin-top: 6px;
            margin-bottom: 0;
            font-size: 12px;
            color: #78350f !important;
            line-height: 1.6;
        }

        /* Footer */
        .footer-card {
            text-align: center;
            padding: 24px 0 10px 0;
            color: #64748b;
            font-size: 13px;
        }
        .footer-link {
            color: #e11d48;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.15s;
        }
        .footer-link:hover {
            color: #be123c;
            text-decoration: underline;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )


    # -------------------------------------------------------------
    # İSTEĞE BAĞLI DİALOG MODALLERİ (YENİLİKLER & REHBER)
    # -------------------------------------------------------------
    @st.dialog("✨ Sürüm Notları ve Yenilikler (v2.0)")
    def show_changelog():
        st.markdown(
            """
            #### 🚀 v2.0 Güncellemesi ile Neler Geldi?
            * **7 Koşuya Genişletildi:** Artık 2'den 7'ye kadar at seçebilir, **Sistem 1'den Sistem 7'ye** tüm kombinasyonları hesaplayabilirsiniz.
            * **🎟️ Bilet (Kart) & Tablo Görünümü:** Kombinasyonlarınızı dijital biletler halinde veya genişletilmiş karşılaştırma tablosunda inceleyebilirsiniz.
            * **Dinamik At Rozetleri:** Her atın kendi başarı durumuna göre (Geldi ✅, Yattı ❌, Bekliyor ⏳) anında renk alması sağlandı.
            * **Canlı Kolon Filtresi:** Yalnızca kazanan veya bekleyen canlı kolonları tek tıkla filtreleyebilirsiniz.
            * **Yenilenen Kokpit:** Kupon maliyeti, misli katsayısı ve finansal özet tek bir hatta toplandı.
            """
        )
        if st.button("Kapat", key="btn_close_chg", use_container_width=True):
            st.rerun()


    @st.dialog("📖 Simülatör Nasıl Kullanılır?")
    def show_guide():
        st.markdown(
            """
            #### 📌 3 Adımda Sistem Bahsi Hesaplama

            1. **Kupon Yapısını Seçin:** 
               * Kuponda kaç at olduğunu belirleyin (2 - 7 arası).
               * Oynamak istediğiniz Sistemleri (S1, S2, S3 vb.) ve Misli katsayınızı işaretleyin.

            2. **Oranları ve Sonuçları Girin:** 
               * Her koşu için en az **Oran** belirlemeniz yeterlidir.
               * Yarış tamamlandıkça durumu **Geldi (Kazandı)** veya **Yattı (Kaybetti)** olarak güncelleyin.

            3. **Sonuçları İnceleyin:** 
               * Canlı kalan kolonlarınızı bilet veya tablo formatında görün.
               * Sayfanın altından **Garantilenen Kazanç** ve **Net Kâr/Zarar** projeksiyonunuzu takip edin.
            """
        )
        if st.button("Anladım", key="btn_close_guide", use_container_width=True):
            st.rerun()


    # SESSION STATE SIFIRLAMA
    def sifirla():
        st.session_state["radio_col_count"] = 4
        st.session_state["num_misli"] = 1

        for s in range(1, 8):
            st.session_state[f"sys{s}"] = s in [1, 2, 3]

        varsayilan_oranlar = [5.50, 1.70, 25.00, 12.00, 3.50, 8.00, 15.00]
        for i in range(7):
            st.session_state[f"name_{i}"] = ""
            st.session_state[f"type_{i}"] = "Ganyan"
            st.session_state[f"oran_{i}"] = varsayilan_oranlar[i]
            st.session_state[f"status_{i}"] = "Bekliyor"


    if "radio_col_count" not in st.session_state:
        sifirla()

    # HERO HEADER & HIZLI ERİŞİM BUTONLARI
    head_title_col, head_action_col = st.columns([3.5, 1.5])
    with head_title_col:
        st.markdown(
            """
            <div class="hero-container" style="margin-bottom:12px; padding: 20px 24px;">
                <div class="hero-title">🏇 Kombine Sistem Bahis Simülatörü</div>
                <p class="hero-subtitle">Koşu ve at kombinasyonlarınızı oluşturun; tüm olasılıkları, kolon tutarlarını ve kazanç projeksiyonlarını anlık hesaplayın.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with head_action_col:
        st.write("&nbsp;")
        b_c1, b_c2 = st.columns(2)
        with b_c1:
            if st.button("✨ Yenilikler", use_container_width=True, help="v2.0 Güncelleme Notları"):
                show_changelog()
        with b_c2:
            if st.button("📖 Rehber", use_container_width=True, help="Nasıl Kullanılır?"):
                show_guide()

    # ADIM 1: KUPON VE SİSTEM YAPISI KOKPİTİ
    with st.container(border=True):
        header_col, reset_col = st.columns([5, 1])
        with header_col:
            st.markdown(
                "<span style='font-size:14px; font-weight:700; color:#334155; text-transform:uppercase; letter-spacing:0.05em;'>⚙️ Kupon Parametreleri & Sistem Seçimi</span>",
                unsafe_allow_html=True,
            )
        with reset_col:
            st.button(
                "🔄 Sıfırla",
                on_click=sifirla,
                use_container_width=True,
                help="Tüm seçimleri varsayılana döndür",
            )

        col_at, col_sistem, col_misli = st.columns([1.1, 2.3, 0.9])

        with col_at:
            st.caption("**Kuponda Kaç At Var?**")
            col_count = st.radio(
                "At Sayısı",
                options=[2, 3, 4, 5, 6, 7],
                key="radio_col_count",
                horizontal=True,
                label_visibility="collapsed",
            )

        with col_sistem:
            st.caption("**Aktif Sistemler**")
            sys_cols = st.columns(7)
            secili_sistemler = {}

            for s in range(1, 8):
                with sys_cols[s - 1]:
                    st.markdown(
                        '<div class="system-pill">', unsafe_allow_html=True
                    )
                    secili_sistemler[s] = st.checkbox(
                        f"S{s}",
                        value=st.session_state.get(
                            f"sys{s}", s <= 3 and s <= col_count
                        ),
                        disabled=(col_count < s),
                        key=f"sys{s}",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

        with col_misli:
            st.caption("**Misli (Katsayı)**")
            misli = st.number_input(
                "Misli",
                min_value=1,
                value=1,
                step=1,
                key="num_misli",
                label_visibility="collapsed",
            )

        kolon_birim_fiyati = 1.0


        def hesapla_bahis_sayisi(at_sayisi):
            toplam_kolon = 0
            at_dummy = list(range(at_sayisi))
            for r in range(1, at_sayisi + 1):
                if secili_sistemler.get(r, False):
                    toplam_kolon += len(list(combinations(at_dummy, r)))
            return toplam_kolon


        bahis_sayisi = hesapla_bahis_sayisi(col_count)
        kupon_bedeli = bahis_sayisi * kolon_birim_fiyati * misli

        # Yüksek Kontrastlı Finansal Çubuk
        st.markdown(
            f"""
            <div class="integrated-kpi-bar">
                <div class="kpi-segment">
                    <span class="kpi-title">Toplam Bahis</span>
                    <span class="kpi-number accent">{bahis_sayisi} <span style="font-size:13px; font-weight:500; color:#cbd5e1;">Kolon</span></span>
                </div>
                <div class="kpi-divider"></div>
                <div class="kpi-segment">
                    <span class="kpi-title">Kupon Misli</span>
                    <span class="kpi-number">{misli} <span style="font-size:13px; font-weight:500; color:#cbd5e1;">Misli</span></span>
                </div>
                <div class="kpi-divider"></div>
                <div class="kpi-segment">
                    <span class="kpi-title">Birim Kolon</span>
                    <span class="kpi-number">{kolon_birim_fiyati:.2f} <span style="font-size:13px; font-weight:500; color:#cbd5e1;">TL</span></span>
                </div>
                <div class="kpi-divider"></div>
                <div class="kpi-segment">
                    <span class="kpi-title">Toplam Kupon Tutarı</span>
                    <span class="kpi-number highlight">{kupon_bedeli:,.2f} <span style="font-size:14px; font-weight:600; color:#6ee7b7;">TL</span></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ADIM 2: AT VE KOŞU DETAYLARI
    st.markdown(
        "<h3 style='font-size:17px; font-weight:700; margin-top:24px; margin-bottom:8px; color:#1e293b;'>📋 Koşu ve Oran Girişleri</h3>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="helper-banner">
            💡 <span><strong>Hızlı İpucu:</strong> Sadece <strong>Oran</strong> girmeniz yeterlidir. İsim ve bahis türü isteğe bağlı detaylardır.</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

    bahis_turleri = [
        "Ganyan",
        "İlk 2",
        "İlk 3",
        "İlk 4",
        "İkili Bahis",
        "Sıralı İkili Bahis",
    ]
    durum_secenekleri = [
        "Bekliyor",
        "Geldi (Kazandı)",
        "Yattı (Kaybetti)",
        "Koşmaz (İade)",
    ]
    varsayilan_oranlar = [5.50, 1.70, 25.00, 12.00, 3.50, 8.00, 15.00]
    at_data = []

    cols_per_row = min(col_count, 4)
    rows_needed = (col_count + cols_per_row - 1) // cols_per_row

    current_idx = 0
    for r in range(rows_needed):
        current_cols_count = min(cols_per_row, col_count - current_idx)
        grid_cols = st.columns(current_cols_count)

        for c in range(current_cols_count):
            i = current_idx
            if f"name_{i}" not in st.session_state:
                st.session_state[f"name_{i}"] = ""
            if f"type_{i}" not in st.session_state:
                st.session_state[f"type_{i}"] = "Ganyan"
            if f"oran_{i}" not in st.session_state:
                st.session_state[f"oran_{i}"] = varsayilan_oranlar[i]
            if f"status_{i}" not in st.session_state:
                st.session_state[f"status_{i}"] = "Bekliyor"

            current_status = st.session_state[f"status_{i}"]
            status_icon = "⏳"
            if current_status == "Geldi (Kazandı)":
                status_icon = "✅"
            elif current_status == "Yattı (Kaybetti)":
                status_icon = "❌"
            elif current_status == "Koşmaz (İade)":
                status_icon = "↩️"

            with grid_cols[c]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="card-header-bar">
                            <span class="selection-title">{status_icon} {i + 1}. Seçim</span>
                            <span class="race-pill">Koşu #{i + 1}</span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    input_c1, input_c2 = st.columns([1, 1.3])

                    with input_c1:
                        st.caption(
                            "**Oran** <span style='color:#e11d48;'>*</span>",
                            unsafe_allow_html=True,
                        )
                        oran = st.number_input(
                            f"Oran {i + 1}",
                            min_value=1.00,
                            step=0.10,
                            key=f"oran_{i}",
                            label_visibility="collapsed",
                        )

                    with input_c2:
                        st.caption("**Sonuç**")
                        durum = st.selectbox(
                            f"Durum {i + 1}",
                            durum_secenekleri,
                            key=f"status_{i}",
                            label_visibility="collapsed",
                        )

                    with st.expander("➕ İsim & Tür Ekle", expanded=False):
                        at_adi = st.text_input(
                            "At Adı",
                            placeholder=f"{i + 1}. At (Opsiyonel)",
                            key=f"name_{i}",
                        )
                        bahis_turu = st.selectbox(
                            "Bahis Türü",
                            options=bahis_turleri,
                            key=f"type_{i}",
                        )

                    label_name = (
                        at_adi.strip()
                        if at_adi.strip() != ""
                        else f"{i + 1}. At"
                    )

                    at_data.append(
                        {
                            "id": i + 1,
                            "ad": label_name,
                            "bahis_turu": bahis_turu,
                            "oran": oran,
                            "durum": durum,
                        }
                    )
            current_idx += 1


    # KOMBİNASYON HESAPLAMA MOTORU
    def hesapla_sistem_gruplari(at_listesi):
        gruplanmis_kombinasyonlar = {}

        for r in range(1, col_count + 1):
            if secili_sistemler.get(r, False):
                kombinasyon_listesi = []

                for comb in combinations(at_listesi, r):
                    kolon_orani = 1.0
                    has_yatti = False
                    has_bekliyor = False

                    at_obj_listesi = []
                    for at in comb:
                        at_obj_listesi.append(
                            {
                                "ad": at["ad"],
                                "bahis_turu": at["bahis_turu"],
                                "durum": at["durum"],
                                "oran": at["oran"],
                            }
                        )

                        if at["durum"] == "Yattı (Kaybetti)":
                            has_yatti = True
                        elif at["durum"] == "Bekliyor":
                            has_bekliyor = True
                            kolon_orani *= at["oran"]
                        elif at["durum"] == "Koşmaz (İade)":
                            kolon_orani *= 1.0
                        else:
                            kolon_orani *= at["oran"]

                    if has_yatti:
                        durum_str = "Kaybetti"
                        durum_class = "lost"
                        badge_html = (
                            '<span class="slip-badge-lost">❌ Kaybetti</span>'
                        )
                        kazanc = 0.00
                    elif has_bekliyor:
                        durum_str = "Bekliyor"
                        durum_class = "pending"
                        badge_html = (
                            '<span class="slip-badge-pending">⏳'
                            " Bekliyor</span>"
                        )
                        kazanc = round(kolon_orani * misli, 2)
                    else:
                        durum_str = "Kazandı"
                        durum_class = "won"
                        badge_html = (
                            '<span class="slip-badge-won">✅ Kazandı</span>'
                        )
                        kazanc = round(kolon_orani * misli, 2)

                    kombinasyon_listesi.append(
                        {
                            "Sistem": f"Sistem {r}",
                            "AtObjeleri": at_obj_listesi,
                            "Kolon Oranı": (
                                round(kolon_orani, 2) if not has_yatti else 0.00
                            ),
                            "Durum": durum_str,
                            "DurumClass": durum_class,
                            "BadgeHTML": badge_html,
                            "Tahmini Kazanç": kazanc,
                        }
                    )

                gruplanmis_kombinasyonlar[r] = pd.DataFrame(kombinasyon_listesi)

        return gruplanmis_kombinasyonlar


    # 1. BİLET KARTLARI GÖRÜNÜMÜ
    def render_native_bet_slips(df_table):
        if df_table.empty:
            st.info("Filtreye uygun kombinasyon bulunamadı.")
            return

        cols_per_slip_row = 3
        rows = [
            df_table.iloc[i: i + cols_per_slip_row]
            for i in range(0, len(df_table), cols_per_slip_row)
        ]

        for row_chunk in rows:
            slip_cols = st.columns(len(row_chunk))
            for col_idx, (_, row) in enumerate(row_chunk.iterrows()):
                border_color = (
                    "#10b981"
                    if row["DurumClass"] == "won"
                    else (
                        "#f59e0b"
                        if row["DurumClass"] == "pending"
                        else "#f43f5e"
                    )
                )

                with slip_cols[col_idx]:
                    with st.container(border=True):
                        st.markdown(
                            f"""
                            <div style="border-left: 4px solid {border_color}; padding-left: 8px; margin-bottom: 8px; display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-size:12px; font-weight:800; color:#334155; text-transform:uppercase; letter-spacing:0.04em;">{row['Sistem']}</span>
                                {row['BadgeHTML']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                        chips_html = '<div style="margin: 10px 0 12px 0; min-height: 48px; display:flex; flex-wrap:wrap; align-items:center;">'
                        for at in row["AtObjeleri"]:
                            at_durum = at["durum"]
                            if at_durum == "Geldi (Kazandı)":
                                chip_class = "chip-at-won"
                                chip_icon = "✅"
                            elif at_durum == "Yattı (Kaybetti)":
                                chip_class = "chip-at-lost"
                                chip_icon = "❌"
                            elif at_durum == "Koşmaz (İade)":
                                chip_class = "chip-at-refund"
                                chip_icon = "↩️"
                            else:
                                chip_class = "chip-at-pending"
                                chip_icon = "⏳"

                            chips_html += f'<span class="{chip_class}">{chip_icon} {at["ad"]} ({at["bahis_turu"]})</span>'
                        chips_html += "</div>"
                        st.markdown(chips_html, unsafe_allow_html=True)

                        payout_color = (
                            "#10b981"
                            if row["DurumClass"] == "won"
                            else (
                                "#0f172a"
                                if row["DurumClass"] == "pending"
                                else "#64748b"
                            )
                        )
                        st.markdown(
                            f"""
                            <div style="display:flex; justify-content:space-between; align-items:flex-end; border-top:1.5px dashed #e2e8f0; padding-top:8px; margin-top:4px;">
                                <div>
                                    <div style="font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase;">KOLON ORANI</div>
                                    <div style="font-size:14px; font-weight:800; color:#0f172a;">{row['Kolon Oranı']:.2f}</div>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:10px; color:#64748b; font-weight:700; text-transform:uppercase;">KAZANÇ / POTANSİYEL</div>
                                    <div style="font-size:16px; font-weight:800; color:{payout_color};">{row['Tahmini Kazanç']:,.2f} TL</div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )


    # 2. TABLO GÖRÜNÜMÜ
    def render_modern_table(df_table, show_system_col=False):
        if df_table.empty:
            return (
                '<div style="padding:24px; text-align:center; color:#64748b;'
                ' font-size:13px;">Filtreye uygun kolon bulunamadı.</div>'
            )

        html = '<div class="table-responsive-wrapper"><div class="modern-table-container"><table class="modern-table"><thead><tr>'
        if show_system_col:
            html += '<th style="width: 100px;">SİSTEM</th>'
        html += "<th>KOMBİNASYONDAKİ ATLAR</th>"
        html += '<th style="width: 110px; text-align:right;">ORAN</th>'
        html += '<th style="width: 130px; text-align:center;">DURUM</th>'
        html += (
            '<th style="width: 160px; text-align:right;">KAZANÇ / POTANSİYEL'
            " (TL)</th>"
        )
        html += "</tr></thead><tbody>"

        for _, row in df_table.iterrows():
            row_class = f"row-{row['DurumClass']}"
            html += f'<tr class="{row_class}">'

            if show_system_col:
                html += f'<td style="font-weight:700; color:#475569;">{row["Sistem"]}</td>'

            chips_html = '<div style="display:flex; flex-wrap:wrap; align-items:center;">'
            for at in row["AtObjeleri"]:
                at_durum = at["durum"]
                if at_durum == "Geldi (Kazandı)":
                    chip_class = "chip-at-won"
                    chip_icon = "✅"
                elif at_durum == "Yattı (Kaybetti)":
                    chip_class = "chip-at-lost"
                    chip_icon = "❌"
                elif at_durum == "Koşmaz (İade)":
                    chip_class = "chip-at-refund"
                    chip_icon = "↩️"
                else:
                    chip_class = "chip-at-pending"
                    chip_icon = "⏳"

                chips_html += f'<span class="{chip_class}">{chip_icon} {at["ad"]} ({at["bahis_turu"]})</span>'
            chips_html += "</div>"
            html += f"<td>{chips_html}</td>"

            html += f'<td style="text-align:right; font-weight:700;">{row["Kolon Oranı"]:.2f}</td>'

            badge_icon = (
                "✅"
                if row["DurumClass"] == "won"
                else "⏳" if row["DurumClass"] == "pending" else "❌"
            )
            html += f'<td style="text-align:center;"><span class="status-badge {row["DurumClass"]}">{badge_icon} {row["Durum"]}</span></td>'

            won_class = "won" if row["DurumClass"] == "won" else ""
            html += f'<td style="text-align:right;" class="payout-val {won_class}">{row["Tahmini Kazanç"]:,.2f} TL</td>'
            html += "</tr>"

        html += "</tbody></table></div></div>"
        return html


    # ADIM 3: KOMBİNASYON VE İKRAMİYE BİLGİSİ
    gruplar = hesapla_sistem_gruplari(at_data)

    if gruplar and any(len(df) > 0 for df in gruplar.values()):
        kesinlesen_kazanc = 0.0
        bekleyen_potansiyel_kazanc = 0.0

        for r, df in gruplar.items():
            kesinlesen_kazanc += df[df["Durum"] == "Kazandı"][
                "Tahmini Kazanç"
            ].sum()
            bekleyen_potansiyel_kazanc += df[df["Durum"] == "Bekliyor"][
                "Tahmini Kazanç"
            ].sum()

        toplam_olasi_kazanc = kesinlesen_kazanc + bekleyen_potansiyel_kazanc
        net_kar_zarar = kesinlesen_kazanc - kupon_bedeli

        # Başlık, Görünüm Seçici ve Filtre
        h_col1, h_col2, h_col3 = st.columns([2.3, 1.2, 1.5])
        with h_col1:
            st.markdown(
                "<h3 style='font-size:17px; font-weight:700; margin-top:20px; margin-bottom:0; color:#1e293b;'>📊 Sistem Kombinasyon Detayları</h3>",
                unsafe_allow_html=True,
            )
        with h_col2:
            view_mode = st.radio(
                "Görünüm Seçimi",
                options=["🎟️ Bilet (Kart)", "📋 Tablo"],
                horizontal=True,
                label_visibility="collapsed",
            )
        with h_col3:
            filtre_durumu = st.selectbox(
                "Durum Filtresi",
                [
                    "Tüm Sonuçlar",
                    "🎯 Canlı Kolonlar (Kazanan + Bekleyen)",
                    "✅ Yalnızca Kazananlar",
                    "⏳ Yalnızca Bekleyenler",
                    "❌ Yalnızca Kaybedenler",
                ],
                label_visibility="collapsed",
            )


        def filtrele_df(df_in):
            if filtre_durumu == "🎯 Canlı Kolonlar (Kazanan + Bekleyen)":
                return df_in[df_in["Durum"].isin(["Kazandı", "Bekliyor"])]
            elif filtre_durumu == "✅ Yalnızca Kazananlar":
                return df_in[df_in["Durum"] == "Kazandı"]
            elif filtre_durumu == "⏳ Yalnızca Bekleyenler":
                return df_in[df_in["Durum"] == "Bekliyor"]
            elif filtre_durumu == "❌ Yalnızca Kaybedenler":
                return df_in[df_in["Durum"] == "Kaybetti"]
            return df_in


        # Sekmeler
        tab_titles = ["📋 Tümü (Konsolide)"] + [
            f"🎯 Sistem {r} ({len(df)})" for r, df in gruplar.items()
        ]
        tabs = st.tabs(tab_titles)

        # Tab 1: Konsolide Liste
        with tabs[0]:
            tum_kombinasyonlar_df = pd.concat(gruplar.values(), ignore_index=True)
            filtrelenmis_tum = filtrele_df(tum_kombinasyonlar_df)

            if view_mode == "🎟️ Bilet (Kart)":
                render_native_bet_slips(filtrelenmis_tum)
            else:
                st.markdown(
                    render_modern_table(filtrelenmis_tum, show_system_col=True),
                    unsafe_allow_html=True,
                )

        # Diğer Tab'lar: Tekil Sistemler
        for idx, (sistem_no, df) in enumerate(gruplar.items()):
            with tabs[idx + 1]:
                filtrelenmis_df = filtrele_df(df)

                if view_mode == "🎟️ Bilet (Kart)":
                    render_native_bet_slips(filtrelenmis_df)
                else:
                    st.markdown(
                        render_modern_table(
                            filtrelenmis_df, show_system_col=False
                        ),
                        unsafe_allow_html=True,
                    )

        # ADIM 4 (FİNAL): SAYFA ALTINDAKİ FİNANSAL İKRAMİYE HERO PANELİ
        if kupon_bedeli > 0:
            roi_orani = (
                                (kesinlesen_kazanc - kupon_bedeli) / kupon_bedeli
                        ) * 100
        else:
            roi_orani = 0.0

        if net_kar_zarar > 0:
            kar_zarar_badge = f"<span style='background:#065f46; color:#34d399; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Net Kâr: +{net_kar_zarar:,.2f} TL (%{roi_orani:,.1f})</span>"
        elif net_kar_zarar < 0:
            kar_zarar_badge = f"<span style='background:#7f1d1d; color:#fca5a5; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Net Zarar: {net_kar_zarar:,.2f} TL</span>"
        else:
            kar_zarar_badge = "<span style='background:#334155; color:#cbd5e1; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Başabaş: 0.00 TL</span>"

        st.markdown(
            f"""
            <div class="payout-hero">
                <div class="payout-grid">
                    <div class="payout-card">
                        <div class="payout-title" style="color: #6ee7b7;">✅ GARANTİLENEN KAZANÇ</div>
                        <div class="payout-amount" style="color: #34d399;">{kesinlesen_kazanc:,.2f} <span style="font-size:16px;">TL</span></div>
                    </div>
                    <div class="payout-card">
                        <div class="payout-title" style="color: #fde047;">⏳ MAKSİMUM OLASI KAZANÇ</div>
                        <div class="payout-amount" style="color: #facc15;">{toplam_olasi_kazanc:,.2f} <span style="font-size:16px;">TL</span></div>
                    </div>
                    <div class="payout-card">
                        <div class="payout-title" style="color: #94a3b8;">KUPON FİNANSAL DURUMU</div>
                        <div style="font-size: 14px; margin-top: 4px; color: #ffffff; font-weight:600;">
                            Maliyet: <strong style="color:#ffffff;">{kupon_bedeli:,.2f} TL</strong>
                        </div>
                        <div style="margin-top: 8px;">
                            {kar_zarar_badge}
                        </div>
                    </div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    else:
        st.info("Kombinasyonları listelemek için en az bir sistem seçiniz.")

    # 4. ORİJİNAL VE TAM YASAL SORUMLULUK REDDİ
    st.markdown(
        """
        <div class="legal-box">
            <p class="legal-title">⚠️ Yasal Uyarı ve Sorumluluk Reddi</p>
            <p class="legal-text">
                Bu simülatör, herhangi bir bahis sitesi veya şans oyunları otoritesi ile resmi bir bağı bulunmaksızın bilgi ve kolaylık sağlama amacıyla bağımsız olarak geliştirilmiştir. 
                Hesaplanan tüm ikramiye ve kolon tutarları kullanıcının girdiği veriler doğrultusunda simüle edilir. Oran değişiklikleri, kesintiler ve nihai bilet sonuçları baş bayi/resmi otorite kurallarına tabidir; sunulan verilerin resmi bir garantisi veya bağlayıcılığı yoktur.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 5. FOOTER
    st.markdown(
        """
        <div class="footer-card">
            Hazırlayan: <strong style="color: #0f172a;">Anıl Şanlı</strong> &nbsp;|&nbsp; 
            <a class="footer-link" href="https://www.linkedin.com/in/anilsanli" target="_blank">LinkedIn</a> &nbsp;•&nbsp; 
            <a class="footer-link" href="https://github.com/anilsanli" target="_blank">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )