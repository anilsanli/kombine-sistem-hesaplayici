from itertools import combinations
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Kombine Sistem Bahis Simülatörü",
    page_icon="🏇",
    layout="wide",
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
    from contextlib import nullcontext

    analytics_context = nullcontext()

with analytics_context:

    # Custom CSS - UI/UX & Renklendirme Düzeltmeleri
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f8f9fa !important;
            color: #1f2937 !important;
        }

        h1, h2, h3, h4, h5, h6, p, label, span {
            color: #1f2937 !important;
        }

        div[data-baseweb="tooltip"],
        div[role="tooltip"],
        div[data-testid="stTooltipContent"] {
            background-color: #0f172a !important;
            color: #ffffff !important;
        }

        div[data-baseweb="input"], 
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 8px !important;
        }

        input, select, textarea {
            color: #0f172a !important;
            background-color: #ffffff !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        div[data-testid="stNumberInput"] button {
            background-color: #f1f5f9 !important;
            color: #0f172a !important;
            border: 1px solid #cbd5e1 !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[role="listbox"],
        div[data-baseweb="popover"] * {
            background-color: #ffffff !important;
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }

        li[role="option"]:hover, 
        li[role="option"][aria-selected="true"] {
            background-color: #f1f5f9 !important;
            color: #e11d48 !important;
            -webkit-text-fill-color: #e11d48 !important;
        }

        div[data-testid="stExpander"] {
            background-color: #ffffff !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 10px !important;
            margin-bottom: 12px !important;
        }

        div[data-testid="stExpander"] details summary {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            border-radius: 10px !important;
        }

        div.stButton > button,
        div.stButton > button * {
            background-color: #e11d48 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: none !important;
        }

        div.stButton > button:hover,
        div.stButton > button:hover * {
            background-color: #be123c !important;
        }

        .horse-card {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 15px;
            border-left: 5px solid #e11d48;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 15px;
        }
        .summary-banner {
            background-color: #ffffff !important;
            border: 1px solid #e2e8f0;
            border-left: 6px solid #e11d48;
            border-radius: 8px;
            padding: 14px 24px;
            margin-top: 15px;
            margin-bottom: 15px;
            display: flex;
            justify-content: space-around;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.03);
        }
        .summary-item {
            font-size: 16px;
            font-weight: 600;
            color: #1f2937 !important;
        }
        .summary-value {
            color: #e11d48 !important;
            font-weight: 700;
        }
        .total-payout-box {
            background-color: #0f172a !important;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            margin-top: 30px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
        }
        .total-payout-box h3, .total-payout-box h1, .total-payout-box p, .total-payout-box span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # SESSION STATE BAŞLANGIÇ DEĞERLERİ & SIFIRLAMA MANTIĞI
    if "reset_trigger" not in st.session_state:
        st.session_state.reset_trigger = False

    def sifirla():
        st.session_state["radio_col_count"] = 4
        st.session_state["sys1"] = True
        st.session_state["sys2"] = True
        st.session_state["sys3"] = True
        st.session_state["sys4"] = False
        st.session_state["num_misli"] = 1

        for i in range(4):
            st.session_state[f"name_{i}"] = ""
            st.session_state[f"type_{i}"] = "Ganyan"
            st.session_state[f"oran_{i}"] = 1.00
            st.session_state[f"status_{i}"] = "Bekliyor"

    st.title("🏇 Kombine Sistem Bahis Hesaplayıcı")
    st.caption(
        "Kombine kuponlarınızda sistem seçeneklerine göre tüm olası"
        " kombinasyonları ve kazançları inceleyin."
    )

    # ADIM 1: KUPON YAPISI VE SİSTEM SEÇİMİ
    head_col1, head_col2 = st.columns([4, 1])
    with head_col1:
        st.markdown("### 1. Kupon ve Sistem Yapısı")
    with head_col2:
        st.button(
            "🔄 Kuponu Sıfırla", on_click=sifirla, use_container_width=True
        )

    col_setup1, col_setup2, col_setup3 = st.columns([1, 2, 1.5])

    with col_setup1:
        col_count = st.radio(
            "Kuponda Kaç At Var?",
            options=[2, 3, 4],
            index=2,
            horizontal=True,
            key="radio_col_count",
            help="Sistem bahsi için en az 2, en fazla 4 at seçilmelidir.",
        )

    with col_setup2:
        st.write("Sistem Seçimi")
        sys_cols = st.columns(4)

        sistem_1 = sys_cols[0].checkbox("Sistem 1", value=True, key="sys1")
        sistem_2 = sys_cols[1].checkbox("Sistem 2", value=True, key="sys2")
        sistem_3 = sys_cols[2].checkbox(
            "Sistem 3",
            value=(col_count >= 3),
            disabled=(col_count < 3),
            key="sys3",
        )
        sistem_4 = sys_cols[3].checkbox(
            "Sistem 4",
            value=(col_count == 4),
            disabled=(col_count < 4),
            key="sys4",
        )

    with col_setup3:
        misli = st.number_input(
            "Misli Seçimi (Katsayı)",
            min_value=1,
            value=1,
            step=1,
            key="num_misli",
            help="Bilet tutarınız ve kazancınız seçtiğiniz misli ile çarpılır.",
        )
        kolon_birim_fiyati = 1.0

    def hesapla_bahis_sayisi(at_sayisi):
        sistem_haritasi = {
            1: sistem_1,
            2: sistem_2,
            3: sistem_3 and at_sayisi >= 3,
            4: sistem_4 and at_sayisi == 4,
        }
        toplam_kolon = 0
        at_dummy = list(range(at_sayisi))
        for r, aktif in sistem_haritasi.items():
            if aktif and r <= at_sayisi:
                toplam_kolon += len(list(combinations(at_dummy, r)))
        return toplam_kolon

    bahis_sayisi = hesapla_bahis_sayisi(col_count)
    kupon_bedeli = bahis_sayisi * kolon_birim_fiyati * misli

    st.markdown(
        f"""
        <div class="summary-banner">
            <div class="summary-item">📌 Bahis Sayısı: <span class="summary-value">{bahis_sayisi} Kolon</span></div>
            <div class="summary-item">✖️ Misli: <span class="summary-value">{misli} Misli</span></div>
            <div class="summary-item">💳 Kupon Bedeli: <span class="summary-value">{kupon_bedeli:,.2f} TL</span></div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.divider()

    # ADIM 2: AT DETAYLARI VE ORAN GİRDİLERİ
    st.markdown("### 2. At ve Koşu Detayları")

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
    at_data = []

    grid_cols = st.columns(col_count)

    for i in range(col_count):
        if f"name_{i}" not in st.session_state:
            st.session_state[f"name_{i}"] = ""
        if f"type_{i}" not in st.session_state:
            st.session_state[f"type_{i}"] = "Ganyan"
        if f"oran_{i}" not in st.session_state:
            st.session_state[f"oran_{i}"] = [5.50, 1.70, 25.00, 12.00][
                i if i < 4 else 0
            ]
        if f"status_{i}" not in st.session_state:
            st.session_state[f"status_{i}"] = "Bekliyor"

        with grid_cols[i]:
            st.markdown(
                f"""
            <div class="horse-card">
                <h4 style="margin:0; color:#1f2937;">{i + 1}. At Seçimi</h4>
            </div>
            """,
                unsafe_allow_html=True,
            )

            at_adi = st.text_input(
                "At Adı (İsteğe Bağlı)",
                placeholder=f"{i + 1}. At",
                key=f"name_{i}",
            )
            bahis_turu = st.selectbox(
                "Bahis Türü (İsteğe Bağlı)",
                options=bahis_turleri,
                key=f"type_{i}",
            )
            oran = st.number_input(
                "Oran (Zorunlu) *",
                min_value=1.00,
                step=0.10,
                key=f"oran_{i}",
            )
            durum = st.selectbox(
                "Sonuç Durumu",
                durum_secenekleri,
                key=f"status_{i}",
            )

            label_name = (
                at_adi.strip() if at_adi.strip() != "" else f"{i + 1}. At"
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

    st.divider()

    # KOMBİNASYON HESAPLAMA MOTORU
    def hesapla_sistem_gruplari(at_listesi):
        sistem_haritasi = {
            1: sistem_1,
            2: sistem_2,
            3: sistem_3 and col_count >= 3,
            4: sistem_4 and col_count == 4,
        }

        gruplanmis_kombinasyonlar = {}

        for r, aktif in sistem_haritasi.items():
            if aktif and r <= len(at_listesi):
                kombinasyon_listesi = []

                for comb in combinations(at_listesi, r):
                    kolon_orani = 1.0
                    has_yatti = False
                    has_bekliyor = False

                    at_detaylari = []
                    for at in comb:
                        at_detaylari.append(f"{at['ad']} ({at['bahis_turu']})")

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
                        durum_str = "❌ Kaybetti"
                        kazanc = 0.00
                    elif has_bekliyor:
                        durum_str = "⏳ Bekliyor"
                        kazanc = round(kolon_orani * misli, 2)
                    else:
                        durum_str = "✅ Kazandı"
                        kazanc = round(kolon_orani * misli, 2)

                    kombinasyon_listesi.append(
                        {
                            "Kombinasyon Detayı": " ➔ ".join(at_detaylari),
                            "Kolon Oranı": (
                                round(kolon_orani, 2) if not has_yatti else 0.00
                            ),
                            "Durum": durum_str,
                            "Tahmini Kazanç": kazanc,
                        }
                    )

                gruplanmis_kombinasyonlar[r] = pd.DataFrame(kombinasyon_listesi)

        return gruplanmis_kombinasyonlar

    def highlight_rows(row):
        if row["Durum"] == "✅ Kazandı":
            return [
                "background-color: #ecfdf5; color: #065f46; font-weight: 600;"
            ] * len(row)
        elif row["Durum"] == "⏳ Bekliyor":
            return [
                "background-color: #fefce8; color: #854d0e; font-weight: 500;"
            ] * len(row)
        elif row["Durum"] == "❌ Kaybetti":
            return [
                "background-color: #fef2f2; color: #991b1b; opacity: 0.8;"
            ] * len(row)
        return [""] * len(row)

    # ADIM 3: SONUÇLAR VE İKRAMİYE BİLGİSİ
    st.markdown("### 3. Kombinasyon ve İkramiye Detayları")

    gruplar = hesapla_sistem_gruplari(at_data)

    if gruplar:
        kesinlesen_kazanc = 0.0
        bekleyen_potansiyel_kazanc = 0.0

        for sistem_no, df in gruplar.items():
            grup_kesin = df[df["Durum"] == "✅ Kazandı"]["Tahmini Kazanç"].sum()
            grup_bekleyen = df[df["Durum"] == "⏳ Bekliyor"][
                "Tahmini Kazanç"
            ].sum()

            kesinlesen_kazanc += grup_kesin
            bekleyen_potansiyel_kazanc += grup_bekleyen

            kazanan_sayisi = len(df[df["Durum"] == "✅ Kazandı"])
            bekleyen_sayisi = len(df[df["Durum"] == "⏳ Bekliyor"])

            expander_title = (
                f"🎯 Sistem {sistem_no} ({sistem_no}'li Kombinasyonlar)  | "
                f" Toplam: {len(df)} Kolon  |  ✅ Kazanan: {kazanan_sayisi}  | "
                f" ⏳ Bekleyen: {bekleyen_sayisi}"
            )

            with st.expander(expander_title, expanded=True):
                styled_df = df.style.apply(highlight_rows, axis=1).format(
                    {"Kolon Oranı": "{:.2f}", "Tahmini Kazanç": "{:,.2f} TL"}
                )

                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Kombinasyon Detayı": st.column_config.TextColumn(
                            "Kombinasyondaki Atlar", width="large"
                        ),
                        "Kolon Oranı": st.column_config.NumberColumn(
                            "Kolon Oranı", format="%.2f"
                        ),
                        "Durum": st.column_config.TextColumn(
                            "Sonuç", width="small"
                        ),
                        "Tahmini Kazanç": st.column_config.TextColumn(
                            "Kazanç / Potansiyel (TL)", width="medium"
                        ),
                    },
                )

        toplam_olasi_kazanc = kesinlesen_kazanc + bekleyen_potansiyel_kazanc
        net_kar_zarar = kesinlesen_kazanc - kupon_bedeli

        if net_kar_zarar > 0:
            kar_durum_metni = (
                f"<span style='color:#34d399;'>Mevcut Net Kâr: +{net_kar_zarar:,.2f}"
                " TL</span>"
            )
        elif net_kar_zarar < 0:
            kar_durum_metni = (
                "<span style='color:#f87171;'>Mevcut Net Zarar:"
                f" {net_kar_zarar:,.2f} TL</span>"
            )
        else:
            kar_durum_metni = (
                "<span style='color:#9ca3af;'>Başabaş (0.00 TL)</span>"
            )

        st.markdown(
            f"""
            <div class="total-payout-box">
                <div style="display: flex; justify-content: space-around; align-items: center; flex-wrap: wrap;">
                    <div>
                        <h3 style="margin:0; font-size: 16px; color: #a5f3fc; font-weight:500;">✅ GARANTİLENEN KAZANÇ</h3>
                        <h1 style="margin:8px 0; font-size: 36px; color: #34d399;">{kesinlesen_kazanc:,.2f} TL</h1>
                    </div>
                    <div style="border-left: 1px solid #334155; height: 50px; margin: 0 20px;"></div>
                    <div>
                        <h3 style="margin:0; font-size: 16px; color: #fef08a; font-weight:500;">⏳ MAKSİMUM OLASI KAZANÇ</h3>
                        <h1 style="margin:8px 0; font-size: 36px; color: #facc15;">{toplam_olasi_kazanc:,.2f} TL</h1>
                    </div>
                </div>
                <p style="margin-top:16px; font-size: 15px; color: #cbd5e1;">Kupon Bedeli: {kupon_bedeli:,.2f} TL &nbsp;|&nbsp; {kar_durum_metni}</p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    else:
        st.info(
            "Lütfen yukarıdan en az bir sistem seçeneğini (Sistem 1, 2 vb.)"
            " işaretleyin."
        )

    # GELİŞTİRİCİ BİLGİSİ / CREDITS
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 10px; color: #64748b; font-size: 14px;">
            Hazırlayan: <strong style="color: #1e293b;">Anıl Şanlı</strong> &nbsp;|&nbsp; 
            <a href="https://www.linkedin.com/in/anilsanli" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">LinkedIn</a> &nbsp;•&nbsp; 
            <a href="https://github.com/anilsanli" target="_blank" style="color: #0284c7; text-decoration: none; font-weight: 600;">GitHub</a>
        </div>
        """,
        unsafe_allow_html=True,
    )