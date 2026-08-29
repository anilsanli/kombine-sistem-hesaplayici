from contextlib import nullcontext

import pandas as pd
import streamlit as st

from logic import (
    BAHIS_TURLERI,
    DURUM_SECENEKLERI,
    KOLON_BIRIM_FIYATI,
    VARSAYILAN_ORANLAR,
    at_chip_bilgisi,
    hesapla_bahis_sayisi,
    hesapla_kupon_bedeli,
    hesapla_sistem_gruplari,
)
from styles import CUSTOM_CSS
from ui_helpers import (
    render_mini_summary,
    render_modern_table,
    render_native_bet_slips,
    uygula_siralama,
)

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
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    # -------------------------------------------------------------
    # İSTEĞE BAĞLI DİALOG MODALLERİ (YENİLİKLER & REHBER)
    # -------------------------------------------------------------
    @st.dialog("✨ Sürüm Notları ve Yenilikler (v2.1)")
    def show_changelog():
        st.markdown(
            """
            #### 🚀 v2.1 Güncellemesi ile Neler Geldi?
            * **↩️ Doğru İade Mantığı:** Bir kolondaki tüm atlar "Koşmaz (İade)" ise artık kolon "Kazandı" değil, doğru şekilde **İade** olarak işaretleniyor.
            * **📊 Sistem Bazlı Özet:** Her sistem sekmesinde o sisteme özel Kesinleşen / Bekleyen / İade tutarları anında görünüyor.
            * **↕️ Sıralama:** Kombinasyonları oran veya kazanca göre büyükten küçüğe / küçükten büyüğe sıralayabilirsiniz.
            * **🧹 Genel Bakım:** Mobil görünüm ve girdi güvenliği (özel karakterler) iyileştirildi.
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
               * Yarış tamamlandıkça durumu **Geldi (Kazandı)**, **Yattı (Kaybetti)** veya **Koşmaz (İade)** olarak güncelleyin.

            3. **Sonuçları İnceleyin:**
               * Canlı kalan kolonlarınızı bilet veya tablo formatında görün, oran/kazanca göre sıralayın.
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

        for i in range(7):
            st.session_state[f"name_{i}"] = ""
            st.session_state[f"type_{i}"] = "Ganyan"
            st.session_state[f"oran_{i}"] = VARSAYILAN_ORANLAR[i]
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
            if st.button("✨ Yenilikler", use_container_width=True, help="v2.1 Güncelleme Notları"):
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

        st.markdown('<div class="mobile-stack-anchor"></div>', unsafe_allow_html=True)
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
                    st.markdown('<div class="system-pill">', unsafe_allow_html=True)
                    secili_sistemler[s] = st.checkbox(
                        f"S{s}",
                        disabled=(col_count < s),
                        key=f"sys{s}",
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

        with col_misli:
            st.caption("**Misli (Katsayı)**")
            misli = st.number_input(
                "Misli",
                min_value=1,
                step=1,
                key="num_misli",
                label_visibility="collapsed",
            )

        bahis_sayisi = hesapla_bahis_sayisi(col_count, secili_sistemler)
        kupon_bedeli = hesapla_kupon_bedeli(bahis_sayisi, misli)

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
                    <span class="kpi-number">{KOLON_BIRIM_FIYATI:.2f} <span style="font-size:13px; font-weight:500; color:#cbd5e1;">TL</span></span>
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
                st.session_state[f"oran_{i}"] = VARSAYILAN_ORANLAR[i]
            if f"status_{i}" not in st.session_state:
                st.session_state[f"status_{i}"] = "Bekliyor"

            current_status = st.session_state[f"status_{i}"]
            _, status_icon = at_chip_bilgisi(current_status)

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
                            DURUM_SECENEKLERI,
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
                            options=BAHIS_TURLERI,
                            key=f"type_{i}",
                        )

                    label_name = at_adi.strip() if at_adi.strip() != "" else f"{i + 1}. At"

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

    # ADIM 3: KOMBİNASYON VE İKRAMİYE BİLGİSİ
    gruplar = hesapla_sistem_gruplari(at_data, col_count, secili_sistemler, misli)

    if gruplar and any(len(df) > 0 for df in gruplar.values()):
        kesinlesen_kazanc = 0.0
        bekleyen_potansiyel_kazanc = 0.0
        iade_tutari = 0.0

        for r, df in gruplar.items():
            kesinlesen_kazanc += df.loc[df["Durum"] == "Kazandı", "Tahmini Kazanç"].sum()
            bekleyen_potansiyel_kazanc += df.loc[df["Durum"] == "Bekliyor", "Tahmini Kazanç"].sum()
            iade_tutari += df.loc[df["Durum"] == "İade", "Tahmini Kazanç"].sum()

        toplam_olasi_kazanc = kesinlesen_kazanc + bekleyen_potansiyel_kazanc
        net_kar_zarar = kesinlesen_kazanc - kupon_bedeli

        # Başlık, Görünüm Seçici, Sıralama ve Filtre
        h_col1, h_col2, h_col3, h_col4 = st.columns([2.0, 1.1, 1.3, 1.3])
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
                    "↩️ Yalnızca İade Edilenler",
                ],
                label_visibility="collapsed",
            )
        with h_col4:
            siralama_secimi = st.selectbox(
                "Sıralama",
                [
                    "Varsayılan",
                    "Kazanç (Yüksek → Düşük)",
                    "Kazanç (Düşük → Yüksek)",
                    "Oran (Yüksek → Düşük)",
                    "Oran (Düşük → Yüksek)",
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
            elif filtre_durumu == "↩️ Yalnızca İade Edilenler":
                return df_in[df_in["Durum"] == "İade"]
            return df_in

        # Sekmeler
        tab_titles = ["📋 Tümü (Konsolide)"] + [f"🎯 Sistem {r} ({len(df)})" for r, df in gruplar.items()]
        tabs = st.tabs(tab_titles)

        # Tab 1: Konsolide Liste
        with tabs[0]:
            tum_kombinasyonlar_df = pd.concat(gruplar.values(), ignore_index=True)
            render_mini_summary(tum_kombinasyonlar_df)
            gorunecek_df = uygula_siralama(filtrele_df(tum_kombinasyonlar_df), siralama_secimi)

            if view_mode == "🎟️ Bilet (Kart)":
                render_native_bet_slips(gorunecek_df)
            else:
                st.markdown(render_modern_table(gorunecek_df, show_system_col=True), unsafe_allow_html=True)

        # Diğer Tab'lar: Tekil Sistemler
        for idx, (sistem_no, df) in enumerate(gruplar.items()):
            with tabs[idx + 1]:
                render_mini_summary(df)
                gorunecek_df = uygula_siralama(filtrele_df(df), siralama_secimi)

                if view_mode == "🎟️ Bilet (Kart)":
                    render_native_bet_slips(gorunecek_df)
                else:
                    st.markdown(render_modern_table(gorunecek_df, show_system_col=False), unsafe_allow_html=True)

        # ADIM 4 (FİNAL): SAYFA ALTINDAKİ FİNANSAL İKRAMİYE HERO PANELİ
        if kupon_bedeli > 0:
            roi_orani = ((kesinlesen_kazanc - kupon_bedeli) / kupon_bedeli) * 100
        else:
            roi_orani = 0.0

        if net_kar_zarar > 0:
            kar_zarar_badge = f"<span style='background:#065f46; color:#34d399; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Net Kâr: +{net_kar_zarar:,.2f} TL (%{roi_orani:,.1f})</span>"
        elif net_kar_zarar < 0:
            kar_zarar_badge = f"<span style='background:#7f1d1d; color:#fca5a5; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Net Zarar: {net_kar_zarar:,.2f} TL</span>"
        else:
            kar_zarar_badge = "<span style='background:#334155; color:#cbd5e1; padding:4px 12px; border-radius:9999px; font-weight:700; font-size:12.5px;'>Başabaş: 0.00 TL</span>"

        iade_satiri = (
            f"<div style='margin-top:6px; font-size:12.5px; color:#94a3b8;'>↩️ İade edilen tutar: <strong style='color:#cbd5e1;'>{iade_tutari:,.2f} TL</strong></div>"
            if iade_tutari > 0
            else ""
        )

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
                        </div>{iade_satiri}
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
